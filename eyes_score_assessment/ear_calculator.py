from dataclasses import dataclass
from typing import List, Tuple

import numpy as np

from .config import *
from .face_mesh_detector import EyeLandmarks


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