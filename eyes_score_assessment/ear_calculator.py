from dataclasses import dataclass
from typing import List, Tuple

import numpy as np

from eyes_score_assessment.ear_config import EAR_MIN, EAR_MAX
from eyes_score_assessment.face_landmark_extractor import EyeLandmarks


@dataclass
class EyeOpennessResult:
    ear_value: float
    openness_percentage: float


def _euclidean_distance(point_a: Tuple[float, float], point_b: Tuple[float, float]) -> float:
    return float(np.linalg.norm(np.array(point_a) - np.array(point_b)))


def calculate_ear(eye: EyeLandmarks) -> float:
    points = eye.points  # [P1, P2, P3, P4, P5, P6]
    p1, p2, p3, p4, p5, p6 = points

    vertical_distance_1 = _euclidean_distance(p2, p6)
    vertical_distance_2 = _euclidean_distance(p3, p5)
    horizontal_distance = _euclidean_distance(p1, p4)

    if horizontal_distance == 0:
        return 0.0

    ear = (vertical_distance_1 + vertical_distance_2) / (2.0 * horizontal_distance)
    return ear


def convert_ear_to_percentage(ear_value: float) -> float:
    normalized = (ear_value - EAR_MIN) / (EAR_MAX - EAR_MIN)
    clamped = np.clip(normalized, 0.0, 1.0)
    return float(clamped * 100.0)


def analyze_eye(eye: EyeLandmarks) -> EyeOpennessResult:
    ear_value = calculate_ear(eye)
    percentage = convert_ear_to_percentage(ear_value)
    return EyeOpennessResult(ear_value=ear_value, openness_percentage=percentage)


def average_ear(left_eye_result: EyeOpennessResult, right_eye_result: EyeOpennessResult) -> EyeOpennessResult:
    avg_ear = (left_eye_result.ear_value + right_eye_result.ear_value) / 2.0
    avg_percentage = (left_eye_result.openness_percentage + right_eye_result.openness_percentage) / 2.0
    return EyeOpennessResult(ear_value=avg_ear, openness_percentage=avg_percentage)


def calculate_image_score(per_face_results: List[EyeOpennessResult]) -> EyeOpennessResult:
    """
    Combines the per-face average EyeOpennessResult (one per detected
    face in the image, i.e. the output of average_ear() for each face)
    into a single overall score for the WHOLE IMAGE.

    Uses a plain average across faces:
      - All faces with closed eyes -> low overall score.
      - One face open among several closed -> score nudges up somewhat,
        but stays weighted down by the closed-eye faces.
      - All faces open -> high overall score.

    This matches the intended behavior: no single face dominates the
    result, but each closed-eye face pulls the overall score down
    proportionally to how many faces are in the photo.
    """
    if not per_face_results:
        raise ValueError("calculate_image_score requires at least one face result")

    avg_ear = float(np.mean([result.ear_value for result in per_face_results]))
    avg_percentage = float(np.mean([result.openness_percentage for result in per_face_results]))

    return EyeOpennessResult(ear_value=avg_ear, openness_percentage=avg_percentage)


def describe_image_score(openness_percentage: float) -> str:
    """
    Simple qualitative label for the final image score, for readability
    in the printed output. Thresholds are illustrative and can be
    tuned freely without affecting the underlying score calculation.
    """
    if openness_percentage >= 75:
        return "excellent - eyes open"
    elif openness_percentage >= 50:
        return "good"
    elif openness_percentage >= 25:
        return "fair - some eyes closed"
    else:
        return "poor - eyes mostly closed"
