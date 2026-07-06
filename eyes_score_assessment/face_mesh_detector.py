"""
face_mesh_detector.py
----------------------
مسؤولية هذا الملف: التعامل مع مكتبة MediaPipe فقط.

هذا الملف يعزل كل التفاصيل الخاصة بـ MediaPipe (تهيئة النموذج، تمرير
الصورة، استخراج الـ landmarks) في مكان واحد. أي ملف آخر في المشروع
لا يحتاج أن "يعرف" أي شيء عن MediaPipe؛ فقط يستدعي هذا الكلاس ويحصل
على إحداثيات نقاط العين جاهزة. هذا يحقق فصل الاهتمامات (Separation
of Concerns) ويجعل استبدال المكتبة مستقبلًا (لو احتجنا) أسهل بكثير.
"""

from dataclasses import dataclass
from typing import List, Tuple

import cv2

import mediapipe as mp
import numpy as np

from config import (
    LEFT_EYE_LANDMARKS,
    RIGHT_EYE_LANDMARKS,
    MAX_NUM_FACES,
    STATIC_IMAGE_MODE,
    MIN_DETECTION_CONFIDENCE,
    REFINE_LANDMARKS,
)


@dataclass
class EyeLandmarks:
    """
    يمثل هذا الكلاس نقاط عين واحدة كإحداثيات (x, y) بالبكسل.
    استخدام dataclass بدل قاموس عادي يجعل الكود أوضح وأكثر أمانًا
    من ناحية الأنواع (type-safety) عند تمريره بين الدوال.
    """
    points: List[Tuple[float, float]]


class NoFaceDetectedError(Exception):
    """استثناء مخصص يُرفع عندما لا يُكتشف أي وجه في الصورة."""
    pass


class FaceMeshDetector:
    """
    غلاف (wrapper) حول MediaPipe Face Mesh.
    مسؤوليته الوحيدة: أخذ صورة وإرجاع نقاط العينين اليسرى واليمنى.
    """

    def __init__(self):
        self._mp_face_mesh = mp.solutions.face_mesh
        self._face_mesh = self._mp_face_mesh.FaceMesh(
            static_image_mode=STATIC_IMAGE_MODE,
            max_num_faces=MAX_NUM_FACES,
            refine_landmarks=REFINE_LANDMARKS,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
        )

    def _extract_landmark_coordinates(
        self,
        face_landmarks,
        landmark_indices: List[int],
        image_width: int,
        image_height: int,
    ) -> List[Tuple[float, float]]:
        """
        تحوّل نقاط MediaPipe (التي تكون كنسب من 0 إلى 1) إلى إحداثيات
        فعلية بالبكسل، بالاعتماد على أبعاد الصورة الأصلية.
        """
        coordinates = []
        for index in landmark_indices:
            landmark = face_landmarks.landmark[index]
            x_pixel = landmark.x * image_width
            y_pixel = landmark.y * image_height
            coordinates.append((x_pixel, y_pixel))
        return coordinates

    def detect_eyes(self, image: np.ndarray) -> Tuple[EyeLandmarks, EyeLandmarks]:
        """
        يستقبل صورة (BGR كما تُقرأ من OpenCV) ويُرجع نقاط العين اليسرى
        واليمنى كإحداثيات بالبكسل.

        يرفع NoFaceDetectedError إذا لم يُكتشف أي وجه في الصورة.
        """
        image_height, image_width = image.shape[:2]

        # MediaPipe يتوقع صورة بصيغة RGB وليس BGR (صيغة OpenCV الافتراضية)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = self._face_mesh.process(rgb_image)

        if not results.multi_face_landmarks:
            raise NoFaceDetectedError(
                "لم يتم اكتشاف أي وجه في الصورة المُدخلة."
            )

        # نأخذ أول وجه مكتشف فقط (المشروع مصمم لصورة تحتوي وجهًا واحدًا)
        face_landmarks = results.multi_face_landmarks[0]

        left_eye_points = self._extract_landmark_coordinates(
            face_landmarks, LEFT_EYE_LANDMARKS, image_width, image_height
        )
        right_eye_points = self._extract_landmark_coordinates(
            face_landmarks, RIGHT_EYE_LANDMARKS, image_width, image_height
        )

        return EyeLandmarks(left_eye_points), EyeLandmarks(right_eye_points)

    def close(self):
        """تحرير موارد MediaPipe عند الانتهاء من الاستخدام."""
        self._face_mesh.close()