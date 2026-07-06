from dataclasses import dataclass
from typing import List, Tuple
import cv2
import mediapipe as mp
import numpy as np

from eyes_score_assessment.config import *


@dataclass
class EyeLandmarks:
    points: List[Tuple[float, float]]


class NoFaceDetectedError(Exception):
    pass


class FaceMeshDetector:

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
    
        coordinates = []
        for index in landmark_indices:
            landmark = face_landmarks.landmark[index]
            x_pixel = landmark.x * image_width
            y_pixel = landmark.y * image_height
            coordinates.append((x_pixel, y_pixel))
        return coordinates

    def detect_eyes(self, image: np.ndarray) -> Tuple[EyeLandmarks, EyeLandmarks]:
        image_height, image_width = image.shape[:2]

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = self._face_mesh.process(rgb_image)

        if not results.multi_face_landmarks:
            raise NoFaceDetectedError(
                "No Face Detected"
            )

        face_landmarks = results.multi_face_landmarks[0]

        left_eye_points = self._extract_landmark_coordinates(
            face_landmarks, LEFT_EYE_LANDMARKS, image_width, image_height
        )
        right_eye_points = self._extract_landmark_coordinates(
            face_landmarks, RIGHT_EYE_LANDMARKS, image_width, image_height
        )

        return EyeLandmarks(left_eye_points), EyeLandmarks(right_eye_points)

    def close(self):
        self._face_mesh.close()