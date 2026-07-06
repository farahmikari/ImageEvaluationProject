from ultralytics import YOLO
import cv2
import os
class PoseDetector:
    def __init__(self, model_path="yolo11n-pose.pt"):
         print("Loading YOLO Pose model...")
         self.model=YOLO(model_path)
         print("Model loaded Successfully")
         self.keypoint_names = [
            "nose",
            "left_eye",
            "right_eye",
            "left_ear",
            "right_ear",
            "left_shoulder",
            "right_shoulder",
            "left_elbow",
            "right_elbow",
            "left_wrist",
            "right_wrist",
            "left_hip",
            "right_hip",
            "left_knee",
            "right_knee",
            "left_ankle",
            "right_ankle"
        ]

    def detect_pose(self,image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Cannot open image : {image_path}")
        results = self.model(image,verbose=False)
        return image, results             

    def extract_keypoints(self,results):
        if len(results) == 0:
            return None

        result = results[0]

        if result.keypoints is None:
            return None

        if len(result.keypoints.xy) == 0:
            return None

        xy = result.keypoints.xy[0].cpu().numpy()

        conf = result.keypoints.conf[0].cpu().numpy()

        keypoints = {}

        for i, name in enumerate(self.keypoint_names):

            keypoints[name] = {
                "x": float(xy[i][0]),
                "y": float(xy[i][1]),
                "confidence": float(conf[i])
            }
        return keypoints

    def draw_keypoints(self,results, output_path):
        annotated = results[0].plot()
        cv2.imwrite(output_path, annotated)
        return annotated 
           
    def get_pose(self, image_path):
     image, results = self.detect_pose(image_path)
     keypoints = self.extract_keypoints(results)
     return image, results, keypoints