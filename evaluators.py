from blur_score_assessment.test import load_model, predict_blur_score
from eyes_score_assessment.face_mesh_detector import FaceMeshDetector, NoFaceDetectedError
from blur_score_assessment.test import predict_blur_score
from eyes_score_assessment.ear_calculator import analyze_eye, average_ear
from eyes_score_assessment.eye_main import load_image
from lighting_assessment import evaluator
from lighting_assessment.evaluator import LightingEvaluator
from body_pose_assessment import assess_pose_aesthetic
import cv2

lighting_evaluator = LightingEvaluator()
eye_detector = FaceMeshDetector()
blur_model = load_model()

def evaluate_blur(image_path):
    score, confidence, _ = predict_blur_score(blur_model, image_path)
    return {
        "clarity_score": score,
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
     left, right = eye_detector.detect_eyes(image)
     left_r = analyze_eye(left)
     right_r = analyze_eye(right)
     overall = average_ear(left_r, right_r)
     return {
        "eye_score": overall.openness_percentage
    }
    except NoFaceDetectedError:
        return {
            "eye_score": None
        }

def evaluate_pose(image_path):
    result = assess_pose_aesthetic(image_path)
    scores=result['score']
    return scores