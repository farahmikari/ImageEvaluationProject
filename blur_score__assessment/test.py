
import argparse
import os
from typing import List, Tuple

import cv2
import numpy as np
import torch
import torch.nn as nn
from torchvision import models


CROP_SIZE = 256
INPUT_SIZE = 224
DROPOUT = 0.3
MODEL_PATH = "./blur_score__assessment/best_blur_model_efficientnet.pth"
DETAIL_WEIGHT_POWER = 0.25
MIN_DETAIL_WEIGHT = 1e-3

IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
IMAGENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def build_model() -> nn.Module:
    model = models.efficientnet_b0(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Linear(in_features, 256),
        nn.ReLU(inplace=True),
        nn.Dropout(DROPOUT),
        nn.Linear(256, 1),
    )
    return model


def load_model(path: str = MODEL_PATH) -> nn.Module:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model weights not found: {path}")

    model = build_model().to(DEVICE)
    state = torch.load(path, map_location=DEVICE)
    model.load_state_dict(state)
    model.eval()
    return model


def read_rgb(img_path: str) -> np.ndarray:
    img_bgr = cv2.imread(img_path, cv2.IMREAD_COLOR)
    if img_bgr is None:
        raise FileNotFoundError(f"Could not read image: {img_path}")
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)


def pad_if_needed(img: np.ndarray, crop_size: int = CROP_SIZE) -> np.ndarray:
    h, w = img.shape[:2]
    if h >= crop_size and w >= crop_size:
        return img
    new_w = max(w, crop_size)
    new_h = max(h, crop_size)
    return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)


def crop_positions(length: int, crop_size: int) -> List[int]:
    if length <= crop_size:
        return [0]
    return sorted(set([0, (length - crop_size) // 2, length - crop_size]))


def extract_crops(img: np.ndarray) -> List[np.ndarray]:
    img = pad_if_needed(img, CROP_SIZE)
    h, w = img.shape[:2]
    ys = crop_positions(h, CROP_SIZE)
    xs = crop_positions(w, CROP_SIZE)

    crops = []
    for top in ys:
        for left in xs:
            crops.append(img[top:top + CROP_SIZE, left:left + CROP_SIZE])
    return crops


def laplacian_detail(patch_rgb: np.ndarray) -> float:
    gray = cv2.cvtColor(patch_rgb, cv2.COLOR_RGB2GRAY)
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())


def preprocess_patch(patch_rgb: np.ndarray) -> torch.Tensor:
    patch = cv2.resize(patch_rgb, (INPUT_SIZE, INPUT_SIZE), interpolation=cv2.INTER_AREA)
    patch = patch.astype(np.float32) / 255.0
    patch = (patch - IMAGENET_MEAN) / IMAGENET_STD
    patch = np.transpose(patch, (2, 0, 1))
    return torch.tensor(patch, dtype=torch.float32)


def predict_blur_score(model: nn.Module, img_path: str, debug: bool = False) -> Tuple[float, float, int]:
    img = read_rgb(img_path)
    crops = extract_crops(img)

    tensors = torch.stack([preprocess_patch(crop) for crop in crops], dim=0).to(DEVICE)
    detail = np.array([laplacian_detail(crop) for crop in crops], dtype=np.float32)

    # Keep detail weighting mild. Severe blur naturally has low Laplacian values;
    # aggressive weighting can make the final score unstable in very blurred images.
    weights = np.power(np.maximum(detail, MIN_DETAIL_WEIGHT), DETAIL_WEIGHT_POWER)
    weights = weights / np.sum(weights)

    with torch.no_grad():
        logits = model(tensors).squeeze(1)
        preds = torch.sigmoid(logits).cpu().numpy()

    clipped = np.clip(preds, 0.0, 1.0)
    score_01 = float(np.sum(clipped * weights))
    confidence = float(np.clip(np.mean(detail) / 500.0, 0.0, 1.0))

    if debug:
        print("  crop_scores:", np.round(clipped * 100.0, 2))
        print("  crop_detail:", np.round(detail, 2))
        print("  crop_weights:", np.round(weights, 3))

    return score_01 * 100.0, confidence, len(crops)


def interpret_score(score: float, confidence: float) -> str:
    if confidence < 0.18:
        return "Low-detail image; score is approximate"
    if score < 20.0:
        return "Very sharp"
    if score < 45.0:
        return "Light blur"
    if score < 70.0:
        return "Medium blur"
    if score < 90.0:
        return "Heavy blur"
    return "Extreme blur"


def pick_images_via_dialog() -> List[str]:
    try:
        from tkinter import Tk, filedialog
    except ImportError as exc:
        raise RuntimeError("tkinter is not available; pass image paths with --images.") from exc

    root = Tk()
    root.withdraw()
    paths = filedialog.askopenfilenames(
        title="Select images",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff")],
    )
    root.destroy()
    return list(paths)


def main() -> None:
    parser = argparse.ArgumentParser(description="Blur Score Inference")
    parser.add_argument("--images", nargs="+", default=None, help="Image paths to analyze.")
    parser.add_argument("--model", default=MODEL_PATH, help="Path to trained model weights.")
    parser.add_argument("--debug", action="store_true", help="Print per-crop scores and weights.")
    args = parser.parse_args()

    try:
        model = load_model(args.model)
        print("Loaded EfficientNet-B0 blur model.")
    except Exception as exc:
        print(exc)
        return

    image_paths = args.images if args.images else pick_images_via_dialog()
    if not image_paths:
        print("No images selected.")
        return

    print("\nBlur score results")
    print("=" * 60)
    for path in sorted(image_paths):
        try:
            score, confidence, crops_count = predict_blur_score(model, path, debug=args.debug)
            label = interpret_score(score, confidence)
            print(f"{os.path.basename(path)}")
            print(f"  Blur Score: {score:.2f}% | confidence: {confidence:.2f} | crops: {crops_count}")
            print(f"  {label}")
        except Exception as exc:
            print(f"Error while processing {path}: {exc}")
        print("-" * 60)


if __name__ == "__main__":
    main()
