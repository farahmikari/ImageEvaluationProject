EPS = 1e-9
CLASS_CENTERS = {"low": 25.0, "medium": 60.0, "high": 90.0}
WEIGHTS = {"lighting": 0.15, "blur": 0.30, "pose": 0.25, "eye_open": 0.30}

LOW_MAX = 45.0
HIGH_MIN = 75.0


def crisp_value_for_criterion(low: float, medium: float, high: float) -> float:
    numerator = (
        low * CLASS_CENTERS["low"]
        + medium * CLASS_CENTERS["medium"]
        + high * CLASS_CENTERS["high"]
    )
    denominator = low + medium + high + EPS
    return round(numerator / denominator, 2)


def weight_of(name: str) -> float:
    return WEIGHTS.get(name, 0.0)


def aggregate_score(
    lighting_value: float, lighting_weight: float,
    blur_value: float, blur_weight: float,
    pose_value: float, pose_weight: float,
    eye_value: float, eye_weight: float,
) -> float:
    total_weight = lighting_weight + blur_weight + pose_weight + eye_weight + EPS
    weighted_sum = (
        lighting_value * lighting_weight
        + blur_value * blur_weight
        + pose_value * pose_weight
        + eye_value * eye_weight
    )
    return round(weighted_sum / total_weight, 2)