import numpy as np
from person_extraction import extract_valid_persons
import os

from siglip_score import compute_siglip_scores_batch

NOSE = 0
L_EYE, R_EYE = 1, 2
L_EAR, R_EAR = 3, 4
L_SHOULDER, R_SHOULDER = 5, 6
L_ELBOW, R_ELBOW = 7, 8
L_WRIST, R_WRIST = 9, 10
L_HIP, R_HIP = 11, 12
L_KNEE, R_KNEE = 13, 14
L_ANKLE, R_ANKLE = 15, 16

def get_point(kp, idx, conf, threshold=0.3):
    if conf[idx] > threshold:
        return kp[idx].numpy() if hasattr(kp[idx], 'numpy') else np.array(kp[idx])
    return None


def euclidean_distance(p1, p2):
    return np.linalg.norm(p1 - p2)


def angle_between_points(p1, p2, p3):
    v1 = p1 - p2
    v2 = p3 - p2
    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-8)
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    return np.degrees(np.arccos(cos_angle))

def line_angle_from_horizontal(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return np.degrees(np.arctan2(dy, dx))

SEGMENT_MASS_RATIOS = {
    "head_trunk": 0.55,   
    "arms": 0.10,         
    "legs": 0.35,          
}
def compute_center_of_mass(kp, conf, threshold=0.3):
    l_shoulder = get_point(kp, L_SHOULDER, conf, threshold)
    r_shoulder = get_point(kp, R_SHOULDER, conf, threshold)
    l_hip = get_point(kp, L_HIP, conf, threshold)
    r_hip = get_point(kp, R_HIP, conf, threshold)
    
    if any(p is None for p in [l_shoulder, r_shoulder, l_hip, r_hip]):
        return None
    trunk_center = (l_shoulder + r_shoulder + l_hip + r_hip) / 4
    
    arm_points = []
    for idx in [L_ELBOW, R_ELBOW, L_WRIST, R_WRIST]:
        p = get_point(kp, idx, conf, threshold)
        if p is not None:
            arm_points.append(p)
    arm_center = np.mean(arm_points, axis=0) if arm_points else trunk_center
    leg_points = []
    for idx in [L_KNEE, R_KNEE, L_ANKLE, R_ANKLE]:
        p = get_point(kp, idx, conf, threshold)
        if p is not None:
            leg_points.append(p)
    leg_center = np.mean(leg_points, axis=0) if leg_points else trunk_center
    com = (trunk_center * SEGMENT_MASS_RATIOS["head_trunk"] +
           arm_center * SEGMENT_MASS_RATIOS["arms"] +
           leg_center * SEGMENT_MASS_RATIOS["legs"])
    
    return com

def build_support_base(kp, conf, threshold=0.3, foot_width_estimate_ratio=0.15, 
                          min_foot_half_width_ratio=0.06):
    l_ankle = get_point(kp, L_ANKLE, conf, threshold)
    r_ankle = get_point(kp, R_ANKLE, conf, threshold)
    
    l_shoulder = get_point(kp, L_SHOULDER, conf, threshold)
    r_shoulder = get_point(kp, R_SHOULDER, conf, threshold)
    if l_shoulder is not None and r_shoulder is not None:
        body_scale = euclidean_distance(l_shoulder, r_shoulder)
    else:
        body_scale = 100
    
    min_half_width = body_scale * min_foot_half_width_ratio
    support_points_x = []
    
    if l_ankle is not None and r_ankle is not None:
     raw_margin = abs(r_ankle[0] - l_ankle[0]) * foot_width_estimate_ratio
     foot_margin = max(raw_margin, min_half_width)
     ankle_min_x = min(l_ankle[0], r_ankle[0])
     ankle_max_x = max(l_ankle[0], r_ankle[0])
     support_points_x = [ankle_min_x - foot_margin, ankle_max_x + foot_margin]
    
    elif l_ankle is not None or r_ankle is not None:
        single_ankle = l_ankle if l_ankle is not None else r_ankle
        support_points_x = [single_ankle[0] - min_half_width, 
                             single_ankle[0] + min_half_width]
    
    else:
        l_hip = get_point(kp, L_HIP, conf, threshold)
        r_hip = get_point(kp, R_HIP, conf, threshold)
        if l_hip is not None and r_hip is not None:
            hip_gap = abs(r_hip[0] - l_hip[0])
            margin = max(hip_gap * foot_width_estimate_ratio, min_half_width * 1.5)  # هامش أكبر قليلاً لأن الوركين أقل دقة من الكاحلين كمؤشر قاعدة
            support_points_x = [min(l_hip[0], r_hip[0]) - margin, max(l_hip[0], r_hip[0]) + margin]
        else:
            return None
    
    return sorted(support_points_x)

def compute_balance_score(kp, conf, threshold=0.3):
    com = compute_center_of_mass(kp, conf, threshold)
    if com is None:
        return None
    
    support_range = build_support_base(kp, conf, threshold)
    if support_range is None:
        return None
    
    base_min_x, base_max_x = support_range
    base_width = base_max_x - base_min_x + 1e-6
    com_x = com[0]
    
    if base_min_x <= com_x <= base_max_x:
        center_of_base = (base_min_x + base_max_x) / 2
        distance_from_center = abs(com_x - center_of_base)
        score = 1.0 - (distance_from_center / base_width) * 0.2 
    else:
        if com_x < base_min_x:
            distance_outside = base_min_x - com_x
        else:
            distance_outside = com_x - base_max_x
        
        normalized_distance = distance_outside / base_width
        score = max(0, 0.8 - normalized_distance)
    return score

def compute_spine_straightness_score(kp, conf, threshold=0.3):
    l_shoulder = get_point(kp, L_SHOULDER, conf, threshold)
    r_shoulder = get_point(kp, R_SHOULDER, conf, threshold)
    l_hip = get_point(kp, L_HIP, conf, threshold)
    r_hip = get_point(kp, R_HIP, conf, threshold)
    
    if any(p is None for p in [l_shoulder, r_shoulder, l_hip, r_hip]):
        return None
    
    shoulder_angle = line_angle_from_horizontal(l_shoulder, r_shoulder)
    hip_angle = line_angle_from_horizontal(l_hip, r_hip)
    
    angle_diff = abs(shoulder_angle - hip_angle)%360
    angle_diff = min(angle_diff, 360 - angle_diff)  
    
    score = max(0, 1 - (angle_diff / 45))  
    return score

def compute_symmetry_score(kp, conf, threshold=0.3):
    scores = []
    
    l_shoulder = get_point(kp, L_SHOULDER, conf, threshold)
    l_elbow = get_point(kp, L_ELBOW, conf, threshold)
    l_wrist = get_point(kp, L_WRIST, conf, threshold)
    r_shoulder = get_point(kp, R_SHOULDER, conf, threshold)
    r_elbow = get_point(kp, R_ELBOW, conf, threshold)
    r_wrist = get_point(kp, R_WRIST, conf, threshold)
    
    if all(p is not None for p in [l_shoulder, l_elbow, l_wrist, r_shoulder, r_elbow, r_wrist]):
        l_elbow_angle = angle_between_points(l_shoulder, l_elbow, l_wrist)
        r_elbow_angle = angle_between_points(r_shoulder, r_elbow, r_wrist)
        diff = abs(l_elbow_angle - r_elbow_angle)
        arm_score = max(0, 1 - abs(diff - 30) / 60)
        scores.append(arm_score)

    l_hip = get_point(kp, L_HIP, conf, threshold)
    l_knee = get_point(kp, L_KNEE, conf, threshold)
    l_ankle = get_point(kp, L_ANKLE, conf, threshold)
    r_hip = get_point(kp, R_HIP, conf, threshold)
    r_knee = get_point(kp, R_KNEE, conf, threshold)
    r_ankle = get_point(kp, R_ANKLE, conf, threshold)
    
    if all(p is not None for p in [l_hip, l_knee, l_ankle, r_hip, r_knee, r_ankle]):
        l_knee_angle = angle_between_points(l_hip, l_knee, l_ankle)
        r_knee_angle = angle_between_points(r_hip, r_knee, r_ankle)
        diff = abs(l_knee_angle - r_knee_angle)
        leg_score = max(0, 1 - abs(diff - 15) / 60)
        scores.append(leg_score)
    
    if len(scores) == 0:
        return None
    
    return np.mean(scores)

def compute_head_angle_score(kp, conf, threshold=0.3):
    nose = get_point(kp, NOSE, conf, threshold)
    l_shoulder = get_point(kp, L_SHOULDER, conf, threshold)
    r_shoulder = get_point(kp, R_SHOULDER, conf, threshold)
    
    if any(p is None for p in [nose, l_shoulder, r_shoulder]):
        return None
    
    shoulder_center = (l_shoulder + r_shoulder) / 2
    
    dx = nose[0] - shoulder_center[0]
    dy = nose[1] - shoulder_center[1]
    angle_from_vertical = np.degrees(np.arctan2(abs(dx), abs(dy) + 1e-6))
    
    tolerance_degrees=15
    max_penalty_degrees=45
    if angle_from_vertical <= tolerance_degrees:
        score = 1.0
    else:
        excess_angle = angle_from_vertical - tolerance_degrees
        penalty_range = max_penalty_degrees - tolerance_degrees
        score = max(0, 1 - (excess_angle / penalty_range))
    return score

def compute_openness_score(kp, conf, threshold=0.3):
    l_wrist = get_point(kp, L_WRIST, conf, threshold)
    r_wrist = get_point(kp, R_WRIST, conf, threshold)
    l_shoulder = get_point(kp, L_SHOULDER, conf, threshold)
    r_shoulder = get_point(kp, R_SHOULDER, conf, threshold)
    
    if any(p is None for p in [l_wrist, r_wrist, l_shoulder, r_shoulder]):
        return None
    
    shoulder_width = euclidean_distance(l_shoulder, r_shoulder) + 1e-6
    wrist_distance = euclidean_distance(l_wrist, r_wrist)
    
    ratio = wrist_distance / shoulder_width
    
    if 1.0 <= ratio <= 2.5:
        score = 1.0
    elif ratio < 1.0:
        score = ratio / 1.0
    else:
        score = max(0, 1 - (ratio - 2.5) / 3)
    return score

def compute_frame_occupancy_score(box_to_frame_ratio):
    if 0.08 <= box_to_frame_ratio <= 0.85:
        return 1.0
    elif box_to_frame_ratio < 0.08:
        return box_to_frame_ratio / 0.08
    else:
        return max(0, 1 - (box_to_frame_ratio - 0.85) / 0.15)

WEIGHTS = {
    "balance": 0.20,
    "spine": 0.15,
    "symmetry": 0.25,
    "head": 0.15,
    "openness": 0.15,
    "occupancy": 0.10,
}


def compute_geometric_score(person_record, conf_threshold=0.3):
    kp = person_record["keypoints_local"]
    conf = person_record["keypoints_conf"]
    
    raw_scores = {
        "balance": compute_balance_score(kp, conf, conf_threshold),
        "spine": compute_spine_straightness_score(kp, conf, conf_threshold),
        "symmetry": compute_symmetry_score(kp, conf, conf_threshold),
        "head": compute_head_angle_score(kp, conf, conf_threshold),
        "openness": compute_openness_score(kp, conf, conf_threshold),
        "occupancy": compute_frame_occupancy_score(person_record["box_to_frame_ratio"]),
    }
    valid_items = {k: v for k, v in raw_scores.items() if v is not None}
    
    if len(valid_items) == 0:
        return None
    
    total_weight = sum(WEIGHTS[k] for k in valid_items)
    final_score = sum(valid_items[k] * WEIGHTS[k] for k in valid_items) / total_weight
    
    return final_score, raw_scores 