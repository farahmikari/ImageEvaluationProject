from pathlib import Path
from pose_detector import PoseDetector
from feature_extractor import FeatureExtractor
from feature_normalizer import FeatureNormalizer
from pprint import pprint

detector=PoseDetector()
extractor=FeatureExtractor()
normalizer=FeatureNormalizer()

BASE_DIR = Path(__file__).resolve().parent

images_folder = BASE_DIR / "images"
outputs_folder = BASE_DIR / "outputs"
results_folder = BASE_DIR / "results"

outputs_folder.mkdir(parents=True, exist_ok=True)
results_folder.mkdir(parents=True, exist_ok=True)

for image_path in images_folder.iterdir():
 if image_path.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
    continue
 print("-" * 60)
 print(image_path.name)
 image,results=detector.detect_pose(str(image_path))
 keypoints=detector.extract_keypoints(results)
 if keypoints is None:
    print("No Person Detected")
    continue

 features=extractor.extract_features(keypoints)
 scores=normalizer.normalize_scores(features)

#  print("Features")
#  pprint(features)
 pprint(scores)
