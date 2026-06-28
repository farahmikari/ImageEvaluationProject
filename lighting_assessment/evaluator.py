from lighting_assessment.metrics import extract_lighting_metrics
from lighting_assessment.scoring import calculate_final_lighting_score
from lighting_assessment.subject_detector import SubjectDetector
from lighting_assessment.roi import create_face_skin_mask


class LightingEvaluator:
    def __init__(self):
        self.detector = SubjectDetector()

    def extract_roi_metrics(self, image):
        roi_metrics = {
            "whole_image": extract_lighting_metrics(image)
        }

        face_landmarks = self.detector.detect_face_landmarks(image)

        if face_landmarks is not None:
            face_skin_mask = create_face_skin_mask(image, face_landmarks)
            face_skin_metrics = extract_lighting_metrics(image, face_skin_mask)

            roi_metrics["face_skin"] = face_skin_metrics

        return roi_metrics

    def evaluate_image(self, image):
        roi_metrics = self.extract_roi_metrics(image)
        scoring_result = calculate_final_lighting_score(roi_metrics)

        return {
            "roi_metrics": roi_metrics,
            "region_scores": scoring_result["region_scores"],
            "final_lighting_score": scoring_result["final_lighting_score"],
        }