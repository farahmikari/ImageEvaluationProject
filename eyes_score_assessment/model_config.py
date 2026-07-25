import os

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_MODELS_DIR = os.path.join(_CURRENT_DIR, "models")

# --- Stage 1: Face detector (full-range, for distant/small faces) ---
# Uses the legacy mp.solutions.face_detection API with model_selection=1.
# No local model file needed - mediapipe downloads/caches it internally.
MIN_DETECTION_CONFIDENCE = 0.5

# --- Stage 2: Face landmarker (mesh points, run on the cropped face) ---
# This path is read directly with Python's open() as bytes and passed to
# mediapipe via model_asset_buffer (see face_landmark_extractor.py), so
# it can safely stay in native Windows/OS format here.
FACE_LANDMARKER_MODEL_PATH = os.path.join(_MODELS_DIR, "face_landmarker.task")
MAX_NUM_FACES = 1
STATIC_IMAGE_MODE = True
REFINE_LANDMARKS = True
MIN_LANDMARK_PRESENCE_CONFIDENCE = 0.5

# --- Crop margin applied around the stage-1 bounding box before stage 2 ---
# Expressed as a fraction of the box's width/height, added on each side.
# This gives the landmark model a close-up-style crop even when the
# original face was small/distant in the source image.
CROP_MARGIN_RATIO = 0.35
