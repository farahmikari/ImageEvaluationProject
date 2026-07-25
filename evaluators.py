from blur_score_assessment.test import load_model, predict_blur_score
from eyes_score_assessment.face_pipeline import FaceMeshDetector, NoFaceDetectedError
from blur_score_assessment.test import predict_blur_score
from body_pose_assessment.feature_extractor import FeatureExtractor
from body_pose_assessment.feature_normalizer import FeatureNormalizer
from body_pose_assessment.pose_detector import PoseDetector
from eyes_score_assessment.ear_calculator import (
    analyze_eye,
    average_ear,
    calculate_image_score,
)
from eyes_score_assessment.eye_main import load_image
from lighting_assessment import evaluator
from lighting_assessment.evaluator import LightingEvaluator
import cv2

pose_detector = PoseDetector()
feature_extractor = FeatureExtractor()
feature_normalizer = FeatureNormalizer()
lighting_evaluator = LightingEvaluator()
eye_detector = FaceMeshDetector()
blur_model = load_model()

def evaluate_blur(image_path):
    result = predict_blur_score(blur_model, image_path)

    return {
        "clarity_score":round(100 - result["overall_score"],2)
    }

def evaluate_lighting(image_path):
    image = cv2.imread(image_path)
    evaluation = lighting_evaluator.evaluate_image(image)
    return {
        "lighting_score": evaluation["final_lighting_score"]
    }

def evaluate_eyes(image_path):
    image = load_image(image_path)
    try:
        all_faces_eyes = eye_detector.detect_eyes(image)

        per_face_overall_results = []

        for left_eye, right_eye in all_faces_eyes:
            left_result = analyze_eye(left_eye)
            right_result = analyze_eye(right_eye)
            overall_result = average_ear(left_result, right_result)
            per_face_overall_results.append(overall_result)

        image_score = calculate_image_score(per_face_overall_results)

        return {
            "eye_score": round(image_score.openness_percentage,2)
        }
    except NoFaceDetectedError:
        return {
            "eye_score": None
        }

def evaluate_pose(image_path):
    image, results = pose_detector.detect_pose(image_path)
    keypoints = pose_detector.extract_keypoints(results)
    if keypoints is None:
        return {
            "pose_score": None
        }
    features = feature_extractor.extract_features(keypoints)
    scores = feature_normalizer.normalize_scores(features)

    return scores