from typing import List, Tuple

import numpy as np

from eyes_score_assessment.face_detector import FaceDetector, NoFaceDetectedError
from eyes_score_assessment.face_landmark_extractor import (
    FaceLandmarkExtractor,
    EyeLandmarks,
    NoLandmarksDetectedError,
)
from eyes_score_assessment.ear_config import LEFT_EYE_LANDMARKS, RIGHT_EYE_LANDMARKS

# Re-exported so existing call sites can keep catching NoFaceDetectedError
# from this module, same as before.
__all__ = ["FaceMeshDetector", "NoFaceDetectedError", "EyeLandmarks"]


class FaceMeshDetector:
    """
    Thin orchestrator preserving the original public interface
    (detect_eyes / close) so ear_calculator.py requires no changes.

    Internally this now runs two stages:
      1. FaceDetector (full-range model) finds ALL face bounding boxes
         in the image, which works reliably even for distant/small faces.
      2. FaceLandmarkExtractor crops around EACH box in turn and
         extracts the fine-grained eye landmarks from that crop.

    detect_eyes() now returns a LIST with one (left_eye, right_eye)
    pair per detected face, in the same order FaceDetector returned the
    boxes in. Callers that only expect a single face should index [0].
    """

    def __init__(self):
        self._face_detector = FaceDetector()
        self._landmark_extractor = FaceLandmarkExtractor()

    def detect_eyes(self, image: np.ndarray) -> List[Tuple[EyeLandmarks, EyeLandmarks]]:
        # Stage 1: locate ALL faces (full-range detector handles distant faces)
        face_boxes = self._face_detector.detect_faces(image)

        results = []
        for face_box in face_boxes:
            # Stage 2: crop around this face and run the landmark model ONCE
            try:
                face_landmarks, crop_box, crop_width, crop_height = (
                    self._landmark_extractor.extract_full_mesh(image, face_box)
                )
            except NoLandmarksDetectedError:
                # This particular face's crop didn't yield usable landmarks
                # (rare - e.g. detector box was too tight/off). Skip it
                # rather than failing the whole image.
                continue

            left_eye = self._landmark_extractor.select_eye_points(
                face_landmarks, crop_box, crop_width, crop_height, LEFT_EYE_LANDMARKS
            )
            right_eye = self._landmark_extractor.select_eye_points(
                face_landmarks, crop_box, crop_width, crop_height, RIGHT_EYE_LANDMARKS
            )
            results.append((left_eye, right_eye))

        if not results:
            raise NoFaceDetectedError("No usable face landmarks found")

        return results

    def close(self):
        self._face_detector.close()
        self._landmark_extractor.close()
