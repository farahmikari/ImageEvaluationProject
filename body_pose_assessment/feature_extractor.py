from utils import *
import math
class FeatureExtractor:
    def __init__(self):
        pass

    def extract_features(self,keypoints):
        torso_height = self.calculate_torso_height(keypoints)
        features = {}
        features["shoulders"] = self.extract_shoulder_features(keypoints,torso_height)
        features["head"] = self.extract_head_features(keypoints)
        features["hands"] = self.extract_hand_features(keypoints)
        features["hips"] = self.extract_hip_features(keypoints,torso_height)
        features["legs"] = self.extract_leg_features(keypoints)
        features["body"] = self.extract_body_features(keypoints,torso_height)
        return features
    
    def calculate_torso_height(self, keypoints):
     left_shoulder = keypoints["left_shoulder"]
     right_shoulder = keypoints["right_shoulder"]
     left_hip = keypoints["left_hip"]
     right_hip = keypoints["right_hip"]

     if not ( 
        is_valid(left_shoulder)and is_valid(right_shoulder)
        and
        is_valid(left_hip) and is_valid(right_hip)):
        return None

     shoulder_center = calculate_center(left_shoulder,right_shoulder)
     hip_center = calculate_center(left_hip,right_hip)

     return distance(
        shoulder_center,
        hip_center
    )

    def extract_shoulder_features(self, keypoints,torso_height):
      left = keypoints["left_shoulder"]
      right = keypoints["right_shoulder"]

      left_visible = is_valid(left)
      right_visible = is_valid(right)
      both_visible = left_visible and right_visible

      angle = None
      difference_ratio = None
      confidence = None

      if both_visible:
        angle = abs(calculate_line_angle(left,right))
        if angle > 90:
            angle = 180 - angle
        if torso_height:
            difference_ratio = ratio(abs(left["y"]-right["y"]),torso_height)

        confidence = average_confidence([left, right])

      return {
        "both_visible": both_visible,
        "angle": angle,
        "difference_ratio": difference_ratio,
        "confidence": confidence
    }
    
    def extract_head_features(self, keypoints):
     nose = keypoints["nose"]
     left_eye = keypoints["left_eye"]
     right_eye = keypoints["right_eye"]

     visible = (is_valid(nose)and is_valid(left_eye) and is_valid(right_eye))
     
     head_angle = None
     confidence = None
     head_visibility=0.0
     if visible:
        head_angle = abs(calculate_line_angle(left_eye,right_eye))
        if head_angle > 90:
            head_angle = 180-head_angle
        head_visibility = visibility_ratio(nose,left_eye,right_eye)
        confidence = average_confidence([nose,left_eye,right_eye])

     return {
        "visible": visible,
        "visibility_ratio":head_visibility,
        "head_angle": head_angle,
        "confidence": confidence
    }
    
    def extract_hand_features(self, keypoints):
     left_wrist = keypoints["left_wrist"]
     right_wrist = keypoints["right_wrist"]
     left_visible = is_valid(left_wrist)
     right_visible = is_valid(right_wrist)
     both_visible = left_visible and right_visible
     hand_visibility = visibility_ratio(left_wrist,right_wrist)
     confidence = average_confidence([left_wrist, right_wrist])

     return {
        "left_visible": left_visible,
        "right_visible": right_visible,
        "both_visible": both_visible,
        "visibility_ratio":hand_visibility,
        "confidence": confidence
    }

    def extract_hip_features(self, keypoints,torso_height):
     left = keypoints["left_hip"]
     right = keypoints["right_hip"]
     left_visible = is_valid(left)
     right_visible = is_valid(right)
     both_visible = left_visible and right_visible
     angle = None
     difference_ratio = None
     confidence = None
     hip_visibility=0.0
     if both_visible:
        angle = abs(calculate_line_angle(left,right))
        if angle > 90:
            angle = 180-angle
        if torso_height:
            difference_ratio = ratio(abs(left["y"]- right["y"] ),torso_height)
        hip_visibility = visibility_ratio(left,right)
        confidence = average_confidence([left, right])

     return {
        "both_visible": both_visible,
        "visibility_ratio":hip_visibility,
        "angle": angle,
        "difference_ratio": difference_ratio,
        "confidence": confidence
    }

    def extract_leg_features(self, keypoints):
     left_knee = keypoints["left_knee"]
     right_knee = keypoints["right_knee"]
     left_ankle = keypoints["left_ankle"]
     right_ankle = keypoints["right_ankle"]
     left_hip = keypoints["left_hip"]
     right_hip = keypoints["right_hip"]

     left_visible = (is_valid(left_knee) and is_valid(left_ankle) and is_valid(left_hip))
     right_visible = (is_valid(right_knee) and is_valid(right_ankle) and is_valid(right_hip))
     both_visible = left_visible and right_visible
     
     left_deviation = None
     right_deviation = None 
     confidence=None   
     leg_visibility=0.0
     if left_visible:
        left_angle=calculate_angle(left_hip,left_knee,left_ankle)
        left_deviation = abs(180-left_angle)
     if right_visible:
        right_angle=calculate_angle(right_hip,right_knee,right_ankle) 
        right_deviation = abs(180-right_angle)
     if both_visible:   
      confidence=average_confidence([left_knee,right_knee,left_ankle,right_ankle])   
      leg_visibility = visibility_ratio(left_knee,right_knee,left_ankle,right_ankle)
 
     return {
        "left_deviation": left_deviation,
        "right_deviation": right_deviation,
        "left_visible": left_visible,
        "right_visible": right_visible,
        "both_visible": both_visible,
        "visibility_ratio":leg_visibility,
        "confidence": confidence
    }

    def extract_body_features(self, keypoints,torso_height):

     left_shoulder = keypoints["left_shoulder"]
     right_shoulder = keypoints["right_shoulder"]
     left_hip = keypoints["left_hip"]
     right_hip = keypoints["right_hip"]

     visible = (
        is_valid(left_shoulder) and is_valid(right_shoulder)
        and
        is_valid(left_hip) and is_valid(right_hip))
     
     torso_angle = None
     offset_ratio = None
     confidence = None

     if visible:
        shoulder_center = calculate_center(left_shoulder,right_shoulder)
        hip_center = calculate_center(left_hip,right_hip)
        torso_angle = calculate_torso_angle(shoulder_center,hip_center)

        if torso_height:
            offset_ratio = ratio(abs(shoulder_center["x"] - hip_center["x"]),torso_height)

        confidence = average_confidence([left_shoulder,right_shoulder,left_hip,right_hip])

     return {
        "visible": visible,
        "torso_angle": torso_angle,
        "offset_ratio": offset_ratio,
        "confidence": confidence
    }    


