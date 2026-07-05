#القيمة الرقمية لكل فئة
ClassType = {"low": 25, "medium": 60, "high": 90}
WEIGHTS = {"lighting": 0.15, "blur": 0.30, "pose": 0.25, "eye_open": 0.30}
EPS = 1e-9
#تستقبل درجات الانتماء
#متوسط موزون بناء على درجات الانتماء لاعطاء سكور الهائي الناتج عن التصنيف
#Weighted Average Defuzzification
def crisp_value_for_criterion(low: float, medium: float, high: float) -> float:
    numerator = low * ClassType["low"] + medium * ClassType["medium"] + high * ClassType["high"]
    denominator = low + medium + high + EPS
    return numerator / denominator
#اعطاء سكور للصورة بناء على معايير اربعة
def final_quality_value(
    lighting_degs: dict, blur_degs: dict, pose_degs: dict, eye_open_degs: dict,
    lighting_weight: float = WEIGHTS["lighting"],
    blur_weight: float = WEIGHTS["blur"],
    pose_weight: float = WEIGHTS["pose"],
    eye_weight: float = WEIGHTS["eye_open"],) -> float:
    lighting_value = crisp_value_for_criterion(**lighting_degs)
    blur_value = crisp_value_for_criterion(**blur_degs)
    pose_value = crisp_value_for_criterion(**pose_degs)
    eye_value = crisp_value_for_criterion(**eye_open_degs)

    total_weight = lighting_weight + blur_weight + pose_weight + eye_weight + EPS

    return round(
        (lighting_weight * lighting_value + blur_weight * blur_value
         + pose_weight * pose_value + eye_weight * eye_value) / total_weight,2,
    )