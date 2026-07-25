from dataclasses import dataclass
from typing import List, Tuple

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python import vision as mp_vision
from mediapipe.tasks.python.vision.core.vision_task_running_mode import (
    VisionTaskRunningMode,
)

from eyes_score_assessment.face_detector import FaceBoundingBox
from eyes_score_assessment.model_config import (
    FACE_LANDMARKER_MODEL_PATH,
    MAX_NUM_FACES,
    MIN_LANDMARK_PRESENCE_CONFIDENCE,
    CROP_MARGIN_RATIO,
)


@dataclass
class EyeLandmarks:
    points: List[Tuple[float, float]]


class NoLandmarksDetectedError(Exception):
    pass


def _expand_box_with_margin(
    box: FaceBoundingBox, image_width: int, image_height: int, margin_ratio: float
) -> FaceBoundingBox:
    box_width = box.x_max - box.x_min
    box_height = box.y_max - box.y_min

    margin_x = int(box_width * margin_ratio)
    margin_y = int(box_height * margin_ratio)

    return FaceBoundingBox(
        x_min=max(0, box.x_min - margin_x),
        y_min=max(0, box.y_min - margin_y),
        x_max=min(image_width, box.x_max + margin_x),
        y_max=min(image_height, box.y_max + margin_y),
    )


class FaceLandmarkExtractor:
    """
    Stage 2 of the pipeline: given an image and a face bounding box
    (from FaceDetector), crops around that box and runs the landmark
    model on the crop only.

    Cropping first is what makes this stage work correctly for distant
    faces: once cropped (with margin), the face fills the frame the same
    way a close-up selfie would, regardless of how small it was in the
    original image. This sidesteps the fact that the landmarker's own
    internal model bundle is not guaranteed to be full-range.

    Landmark coordinates are mapped back to the ORIGINAL image's pixel
    space before being returned, so callers never need to think about
    the crop.
    """

    def __init__(self):
        # Loaded as a bytes buffer (model_asset_buffer) rather than a file
        # path (model_asset_path). This sidesteps a mediapipe bug on
        # Windows where absolute paths get incorrectly concatenated with
        # an internal package resource directory, producing a malformed
        # path (a stray ":" outside the drive-letter position) that
        # Windows' file APIs reject with errno=22 ("invalid argument"),
        # even though the file exists and the path is otherwise correct.
        with open(FACE_LANDMARKER_MODEL_PATH, "rb") as model_file:
            model_bytes = model_file.read()

        base_options = BaseOptions(model_asset_buffer=model_bytes)
        options = mp_vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=VisionTaskRunningMode.IMAGE,
            num_faces=MAX_NUM_FACES,
            min_face_presence_confidence=MIN_LANDMARK_PRESENCE_CONFIDENCE,
            output_face_blendshapes=False,
            output_facial_transformation_matrixes=False,
        )
        self._landmarker = mp_vision.FaceLandmarker.create_from_options(options)

    def extract_full_mesh(self, image: np.ndarray, face_box: FaceBoundingBox):
        """
        Runs the landmark model ONCE on the crop and returns the raw
        mesh result plus the crop geometry needed to map coordinates
        back to the original image. Call this once per face; use
        select_eye_points() below to pull out specific landmark subsets
        without re-running inference.
        """
        image_height, image_width = image.shape[:2]

        crop_box = _expand_box_with_margin(
            face_box, image_width, image_height, CROP_MARGIN_RATIO
        )

        cropped_image = image[crop_box.y_min:crop_box.y_max, crop_box.x_min:crop_box.x_max]
        crop_height, crop_width = cropped_image.shape[:2]

        rgb_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_crop)

        result = self._landmarker.detect(mp_image)

        if not result.face_landmarks:
            raise NoLandmarksDetectedError("No landmarks detected in cropped face region")

        face_landmarks = result.face_landmarks[0]
        return face_landmarks, crop_box, crop_width, crop_height

    def select_eye_points(
        self,
        face_landmarks,
        crop_box: FaceBoundingBox,
        crop_width: int,
        crop_height: int,
        landmark_indices: List[int],
    ) -> EyeLandmarks:
        points = []
        for index in landmark_indices:
            landmark = face_landmarks[index]
            # Landmark coordinates are normalized to the CROP; convert to
            # crop pixel space, then offset back into the original image.
            x_in_original = crop_box.x_min + (landmark.x * crop_width)
            y_in_original = crop_box.y_min + (landmark.y * crop_height)
            points.append((x_in_original, y_in_original))

        return EyeLandmarks(points)

    def close(self):
        self._landmarker.close()
