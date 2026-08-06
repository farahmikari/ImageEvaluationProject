TEST_FOLDER="test_photos"

YOLO_MODEL_PATH = "models/yolo11s-pose.pt"
YOLO_IMGSZ = 1280
MIN_VALID_KEYPOINTS = 8
KEYPOINT_CONF_THRESHOLD = 0.3
CONTAINMENT_THRESHOLD = 0.7
CROP_MARGIN_RATIO = 0.08
IOU_DEDUP_THRESHOLD = 0.5

GEOMETRIC_WEIGHTS = {
    "balance": 0.20,
    "spine": 0.15,
    "symmetry": 0.25,
    "head": 0.15,
    "openness": 0.15,
    "occupancy": 0.10,
}

SIGLIP_MODEL_NAME = "google/siglip2-base-patch16-224"

PROMPT_PAIRS = [
    {
        "positive": "a person standing in a natural, balanced, graceful pose",
        "negative": "a person standing in a stiff, awkward, unnatural pose",
        "weight": 1.0,
    },
    {
        "positive": "a person photographed with professional, aesthetically pleasing body positioning",
        "negative": "a person photographed with poor, unflattering body positioning",
        "weight": 1.0,
    },
    {
        "positive": "a dynamic pose with interesting body angles and visual movement",
        "negative": "a flat, static pose with no visual interest or movement",
        "weight": 1.0,
    },
    {
        "positive": "an exceptionally well-posed, magazine-quality body position",
        "negative": "a completely unposed, snapshot-quality body position",
        "weight": 1.0,
    },
    {
        "positive": "a person in an engaging pose",
        "negative": "a person in a dull pose",
        "weight": 1.0,
    },
    {
        "positive": "a person in a relaxed pose",
        "negative": "a person in a tense pose",
        "weight": 1.0,
    },
]

SIGLIP_CALIBRATION_MIN = 0.2006
SIGLIP_CALIBRATION_MAX = 0.6418
SIGLIP_CALIBRATION_SOFTNESS = 0.02

FUSION_WEIGHTS = {
    "geometric": 0.55,
    "siglip": 0.45,
}
DISAGREEMENT_THRESHOLD = 0.55
DISAGREEMENT_PENALTY_FACTOR = 0.15
TRUST_RATIO = 0.85 
CALIBRATION_MIN = 0.15
CALIBRATION_MAX = 0.90

SIZE_WEIGHT_POWER = 1.0
DISPERSION_THRESHOLD = 25.0
DISPERSION_PENALTY_FACTOR = 0.15

MINIMUM_RELIABLE_SCORE = 40.0

MIN_OCCUPANCY_FOR_MAIN_SUBJECT = 0.05 