from ultralytics import YOLO
import numpy as np
from PIL import Image
import os
model = YOLO("models/yolo11s-pose.pt")

def run_pose_detection(image_path):
    results=model(image_path,verbose=False )
    return results[0]

def is_valid_person(kp_conf, min_valid=8, threshold=0.3):
    valid_count = (kp_conf > threshold).sum().item()
    return valid_count >= min_valid, valid_count


def containment_ratio(small_box, big_box):
    x1 = max(small_box[0], big_box[0])
    y1 = max(small_box[1], big_box[1])
    x2 = min(small_box[2], big_box[2])
    y2 = min(small_box[3], big_box[3])
    
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    small_area = (small_box[2] - small_box[0]) * (small_box[3] - small_box[1])
    
    return inter / small_area if small_area > 0 else 0


def filter_contained_boxes(boxes, ratio_threshold=0.5):
    n = len(boxes)
    excluded = set()
    
    for i in range(n):
        for j in range(n):
            if i == j or i in excluded:
                continue
            area_i = (boxes[i][2]-boxes[i][0]) * (boxes[i][3]-boxes[i][1])
            area_j = (boxes[j][2]-boxes[j][0]) * (boxes[j][3]-boxes[j][1])

            if area_i < area_j:
                ratio = containment_ratio(boxes[i], boxes[j])
                if ratio > ratio_threshold:
                    excluded.add(i)
    
    return excluded

def build_box_from_keypoints(kp_xy, kp_conf, threshold=0.15, margin_ratio=0.08,
                             extra_top_margin_ratio=0.15, img_w=None, img_h=None):
    mask = kp_conf > threshold
    valid_points = kp_xy[mask]
    
    x_min = valid_points[:, 0].min().item()
    y_min = valid_points[:, 1].min().item()
    x_max = valid_points[:, 0].max().item()
    y_max = valid_points[:, 1].max().item()
    
    w = x_max - x_min
    h = y_max - y_min
    
    x_min -= w * margin_ratio
    x_max += w * margin_ratio
    y_min -= h * (margin_ratio+extra_top_margin_ratio)
    y_max += h * margin_ratio
    
    if img_w is not None:
        x_min = max(0, x_min)
        x_max = min(img_w, x_max)
    if img_h is not None:
        y_min = max(0, y_min)
        y_max = min(img_h, y_max)
    
    return int(x_min), int(y_min), int(x_max), int(y_max)

def crop_person(image, box, kp_xy):
    x_min, y_min, x_max, y_max = box
    cropped_image = image.crop((x_min, y_min, x_max, y_max))
    local_kp = kp_xy.clone()
    local_kp[:, 0] -= x_min
    local_kp[:, 1] -= y_min
    return cropped_image, local_kp 
  
def build_person_record(person_idx, cropped_image, local_kp, original_kp, kp_conf, 
                          valid_count, box, img_w, img_h):
    box_area = (box[2] - box[0]) * (box[3] - box[1])
    frame_area = img_w * img_h
    return {
        "person_id": person_idx,
        "crop_image": cropped_image,          
        "keypoints_local": local_kp,            
        "keypoints_original": original_kp,      
        "keypoints_conf": kp_conf,
        "valid_points_count": valid_count,      
        "box": box,
        "box_to_frame_ratio": box_area / frame_area,  
    } 
def extract_valid_persons(image_path, min_valid_points=8, kp_threshold=0.3, 
                            containment_threshold=0.7):
    r = run_pose_detection(image_path)
    
    if r.keypoints is None or len(r.keypoints.xy) == 0:
        return []  
    image = Image.open(image_path).convert("RGB")
    img_w, img_h = image.size
    
    kp_xy_all = r.keypoints.xy          
    kp_conf_all = r.keypoints.conf      
    
    candidates = []
    for i in range(len(kp_xy_all)):
        valid, count = is_valid_person(kp_conf_all[i], min_valid_points, kp_threshold)
        if valid:
            candidates.append(i)
    
    if len(candidates) == 0:
        return []
    temp_boxes = []
    for i in candidates:
        box = build_box_from_keypoints(
            kp_xy_all[i], kp_conf_all[i], 
            threshold=kp_threshold, img_w=img_w, img_h=img_h
        )
        temp_boxes.append(box)

    excluded_local = filter_contained_boxes(temp_boxes, containment_threshold)
    
    final_candidates = [candidates[i] for i in range(len(candidates)) if i not in excluded_local]
    final_boxes = [temp_boxes[i] for i in range(len(temp_boxes)) if i not in excluded_local]
    
    person_records = []
    for idx, (person_i, box) in enumerate(zip(final_candidates, final_boxes)):
        cropped_image, local_kp = crop_person(image, box, kp_xy_all[person_i])
        _, valid_count = is_valid_person(kp_conf_all[person_i], min_valid_points, kp_threshold)
        
        record = build_person_record(
            person_idx=idx,
            cropped_image=cropped_image,
            local_kp=local_kp,
            original_kp=kp_xy_all[person_i],
            kp_conf=kp_conf_all[person_i],
            valid_count=valid_count,
            box=box,
            img_w=img_w,
            img_h=img_h
        )
        person_records.append(record)
    
    return person_records


