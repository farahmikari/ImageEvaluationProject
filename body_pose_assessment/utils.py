from enum import Enum
from config import *
import math
def normalize(value, best, worst):
    if value is None:
        return None
    value=abs(value)
    if value <= best:
        return 100.0
    if value >= worst:
        return 0.0
    score = 100 * (worst - value) / (worst - best)
    return round(score, 2)

def is_valid(kp):
    return kp is not None and kp["confidence"] >= MIN_CONFIDENCE

def distance(point1, point2):
    return math.sqrt(
        (point1["x"]-point2["x"])**2 +
        (point1["y"]-point2["y"])**2
    )

def calculate_center(point1, point2):
    return {
        "x": (point1["x"]+point2["x"])/2,
        "y": (point1["y"]+point2["y"])/2
    }

def calculate_line_angle(point1, point2):
    return math.degrees(
        math.atan2(
            point2["y"]-point1["y"],
            point2["x"]-point1["x"]
        )
    )

def calculate_torso_angle(shoulder_center,hip_center):
    angle = math.degrees(
        math.atan2(
            hip_center["y"]-shoulder_center["y"],
            hip_center["x"]-shoulder_center["x"]
        ))
    angle = abs(90-angle)
    return angle

def calculate_angle(point1,point2, point3):
    a = distance(point2, point3)
    b = distance(point1, point3)
    c = distance(point1, point2)
    if a == 0 or c == 0:
        return None
    value = (a*a +c*c -b*b) / (2*a*c)
    value = max(-1,min(1,value))
    angle = math.degrees(math.acos(value))
    return angle    

def average_confidence(points):
    confidences = [point["confidence"] for point in points if point is not None]
    if len(confidences)==0:
        return 0
    return sum(confidences)/len(confidences)

def ratio(value, reference):
    if reference == 0:
        return None
    return value/reference

def visibility_ratio(*points):
    if len(points) == 0:
        return 0.0

    visible = sum(
        1
        for point in points
        if is_valid(point)
    )

    return visible / len(points)

class EvaluationLevel(Enum):
    EXCELLENT = "EXCELLENT"
    GOOD = "GOOD"
    FAIR = "FAIR"
    POOR = "POOR"
    NOT_EVALUATED = "NOT_EVALUATED"
    # //////////////////////////////////////////////////
def weighted_average(values):
    total_score = 0
    total_weight = 0

    for score, weight in values:

        if score is None:
            continue

        total_score += score * weight
        total_weight += weight

    if total_weight == 0:
        return None

    return round(total_score/total_weight,2)

def normalize_result(score,valid=True,confidence=None, reason=EvaluationReason.OK):
    return {
        "score": score,
        "reason": reason
    }