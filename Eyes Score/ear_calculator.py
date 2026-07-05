"""
ear_calculator.py
-------------------
مسؤولية هذا الملف: العمليات الرياضية البحتة فقط.

هذا الملف لا يعرف شيئًا عن MediaPipe ولا عن الصور؛ كل ما يهتم به هو:
معطى مجموعة من 6 نقاط (إحداثيات x, y)، احسب قيمة EAR، ثم حوّلها إلى
نسبة مئوية. فصل المنطق الرياضي عن منطق استخراج البيانات يجعل هذا
الجزء قابلاً للاختبار (unit testing) بسهولة تامة دون الحاجة لصورة
حقيقية أو حتى لمكتبة MediaPipe.
"""

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np

from config import EAR_MIN, EAR_MAX
from face_mesh_detector import EyeLandmarks


@dataclass
class EyeOpennessResult:
    """
    يمثل نتيجة نهائية لعين واحدة: قيمة EAR الخام ونسبة الانفتاح المئوية.
    """
    ear_value: float
    openness_percentage: float


def _euclidean_distance(point_a: Tuple[float, float], point_b: Tuple[float, float]) -> float:
    """يحسب المسافة الإقليدية بين نقطتين (x, y)."""
    return float(np.linalg.norm(np.array(point_a) - np.array(point_b)))


def calculate_ear(eye: EyeLandmarks) -> float:
    """
    يحسب قيمة Eye Aspect Ratio (EAR) بناءً على معادلة
    Soukupová & Čech (2016):

        EAR = (‖P2 - P6‖ + ‖P3 - P5‖) / (2 * ‖P1 - P4‖)

    حيث:
    - P1, P4: زوايا العين (البعد الأفقي)
    - P2, P3: نقاط الجفن العلوي
    - P5, P6: نقاط الجفن السفلي

    كلما اقتربت العين من الانغلاق التام، تقترب القيمة من الصفر.
    كلما كانت العين مفتوحة بالكامل، ترتفع القيمة (عادة بين 0.25 و 0.35).
    """
    points = eye.points  # [P1, P2, P3, P4, P5, P6]
    p1, p2, p3, p4, p5, p6 = points

    vertical_distance_1 = _euclidean_distance(p2, p6)
    vertical_distance_2 = _euclidean_distance(p3, p5)
    horizontal_distance = _euclidean_distance(p1, p4)

    # حماية من القسمة على صفر في حال كانت النقاط متطابقة خطأً
    if horizontal_distance == 0:
        return 0.0

    ear = (vertical_distance_1 + vertical_distance_2) / (2.0 * horizontal_distance)
    return ear


def convert_ear_to_percentage(ear_value: float) -> float:
    """
    يحوّل قيمة EAR الخام إلى نسبة مئوية بين 0% و100%، بالاعتماد على
    حدين مرجعيين EAR_MIN (عين مغلقة) و EAR_MAX (عين مفتوحة بالكامل)،
    المعرّفين في config.py.

    نستخدم np.clip لضمان أن الناتج يبقى دائمًا ضمن [0, 100] حتى لو
    خرجت قيمة EAR الفعلية عن الحدود المتوقعة (بسبب زاوية وجه غير
    اعتيادية مثلاً).
    """
    normalized = (ear_value - EAR_MIN) / (EAR_MAX - EAR_MIN)
    clamped = np.clip(normalized, 0.0, 1.0)
    return float(clamped * 100.0)


def analyze_eye(eye: EyeLandmarks) -> EyeOpennessResult:
    """
    الدالة العامة التي تجمع الخطوتين معًا: حساب EAR ثم تحويله لنسبة.
    هذه هي نقطة الدخول الوحيدة التي يحتاجها بقية المشروع من هذا الملف.
    """
    ear_value = calculate_ear(eye)
    percentage = convert_ear_to_percentage(ear_value)
    return EyeOpennessResult(ear_value=ear_value, openness_percentage=percentage)


def average_ear(left_eye_result: EyeOpennessResult, right_eye_result: EyeOpennessResult) -> EyeOpennessResult:
    """
    يحسب متوسط EAR ونسبة الانفتاح بين العينين، وهو الناتج النهائي
    الذي يُعرض عادة للمستخدم كقيمة واحدة تمثل حالة الوجه ككل.
    """
    avg_ear = (left_eye_result.ear_value + right_eye_result.ear_value) / 2.0
    avg_percentage = (left_eye_result.openness_percentage + right_eye_result.openness_percentage) / 2.0
    return EyeOpennessResult(ear_value=avg_ear, openness_percentage=avg_percentage)