from dataclasses import dataclass
from typing import List

import cv2
import mediapipe as mp
import numpy as np

from eyes_score_assessment.model_config import MIN_DETECTION_CONFIDENCE


@dataclass
class FaceBoundingBox:
    x_min: int
    y_min: int
    x_max: int
    y_max: int


class NoFaceDetectedError(Exception):
    pass


class FaceDetector:
    """
    Stage 1 of the pipeline: locates face bounding boxes in an image.

    NOTE: This uses the LEGACY mp.solutions.face_detection API rather
    than the modern Tasks API FaceDetector. This is a deliberate choice,
    not an oversight: as of mediapipe 0.10.x, loading the standalone
    blaze_face_full_range.tflite model into the Tasks API FaceDetector
    triggers a confirmed, unresolved internal bug (RET_CHECK failure in
    TensorsToDetectionsCalculator - the graph's anchor/box-count config
    is hardcoded for the short-range model's tensor shape and does not
    match the full-range model's output). See:
    https://github.com/google-ai-edge/mediapipe/issues/5844

    The legacy solutions API has a purpose-built graph for the
    full-range model, selected via model_selection=1, and does not hit
    this bug. That's what's used here.
    """

    def __init__(self):
        self._mp_face_detection = mp.solutions.face_detection
        self._detector = self._mp_face_detection.FaceDetection(
            model_selection=1,  # 0 = short-range (~2m), 1 = full-range (~5m)
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
        )

    def detect_faces(self, image: np.ndarray) -> List[FaceBoundingBox]:
        image_height, image_width = image.shape[:2]

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self._detector.process(rgb_image)

        if not results.detections:
            raise NoFaceDetectedError("No Face Detected")

        boxes = []
        for detection in results.detections:
            relative_box = detection.location_data.relative_bounding_box

            x_min = max(0, int(relative_box.xmin * image_width))
            y_min = max(0, int(relative_box.ymin * image_height))
            x_max = min(image_width, int((relative_box.xmin + relative_box.width) * image_width))
            y_max = min(image_height, int((relative_box.ymin + relative_box.height) * image_height))

            boxes.append(FaceBoundingBox(x_min, y_min, x_max, y_max))

        return boxes

    def close(self):
        self._detector.close()
