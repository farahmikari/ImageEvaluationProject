"""
Blur score inference script.

Goal: estimate the OVERALL blur percentage of the whole photo (how much
of the image is blurry), not just flag a single bad region and not let
sharp regions hide blurry ones either.

The final score is the SIMPLE (unweighted) average of the per-crop
predictions. The crop grid (3x3 positions: start/middle/end on each
axis) covers the image edge-to-edge, so an unweighted average is a fair
estimate of "how blurry is the image as a whole". We deliberately do
NOT use detail-weighted averaging (would let sharp regions mask real
blur elsewhere) and do NOT report only the worst crop (would overstate
overall blur from one bad corner). Both worst-crop and best-crop are
still reported alongside the average purely as diagnostic info, to help
you see how uniform the blur is across the frame.

Preprocessing here mirrors train.py's normalize_patch() and padding logic
exactly (same crop size, input size, interpolation methods, and
ImageNet normalization) so the model sees the same kind of input at
inference time as it did during training/validation.
"""

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
MODEL_PATH = "./blur_score_assessment/best_blur_model_efficientnet.pth"

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
    # Same approach as train.py: upscale (INTER_CUBIC) rather than pad with
    # black borders, so we never feed the model an artificial hard edge.
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


def extract_crops(img: np.ndarray) -> List[Tuple[np.ndarray, int, int]]:
    """Returns (patch, top, left) so callers can report WHERE a blurred
    region is located in the original image, not just an aggregate score."""
    img = pad_if_needed(img, CROP_SIZE)
    h, w = img.shape[:2]
    ys = crop_positions(h, CROP_SIZE)
    xs = crop_positions(w, CROP_SIZE)

    crops = []
    for top in ys:
        for left in xs:
            patch = img[top:top + CROP_SIZE, left:left + CROP_SIZE]
            crops.append((patch, top, left))
    return crops


def preprocess_patch(patch_rgb: np.ndarray) -> torch.Tensor:
    # Mirrors train.py normalize_patch() exactly: same target size,
    # same interpolation (INTER_AREA), same ImageNet mean/std.
    patch = cv2.resize(patch_rgb, (INPUT_SIZE, INPUT_SIZE), interpolation=cv2.INTER_AREA)
    patch = patch.astype(np.float32) / 255.0
    patch = (patch - IMAGENET_MEAN) / IMAGENET_STD
    patch = np.transpose(patch, (2, 0, 1))
    return torch.tensor(patch, dtype=torch.float32)


def predict_blur_score(model: nn.Module, img_path: str, debug: bool = False) -> dict:
    img = read_rgb(img_path)
    crops = extract_crops(img)
    patches = [c[0] for c in crops]

    tensors = torch.stack([preprocess_patch(p) for p in patches], dim=0).to(DEVICE)

    with torch.no_grad():
        logits = model(tensors).squeeze(1)
        preds = torch.sigmoid(logits).cpu().numpy()

    scores_pct = np.clip(preds, 0.0, 1.0) * 100.0

    # Primary result: simple unweighted average across all crops. The 3x3
    # grid covers the frame edge-to-edge, so this is a fair estimate of
    # the blur percentage of the WHOLE image, without letting sharp
    # regions dilute real blur elsewhere (no detail weighting) and
    # without letting a single bad corner dominate the whole-image score
    # (no worst-only reporting).
    overall_score = float(np.mean(scores_pct))
    median_score = float(np.median(scores_pct))
    std_score = float(np.std(scores_pct))

    # Diagnostic-only info: how uniform is the blur across the frame?
    worst_idx = int(np.argmax(scores_pct))
    best_idx = int(np.argmin(scores_pct))
    worst_score = float(scores_pct[worst_idx])
    best_score = float(scores_pct[best_idx])
    worst_top, worst_left = crops[worst_idx][1], crops[worst_idx][2]

    if debug:
        print("  per-crop scores %:", np.round(scores_pct, 2))
        print("  per-crop positions (top,left):", [(c[1], c[2]) for c in crops])

    return {
        "overall_score": overall_score,
        "median_score": median_score,
        "std_score": std_score,
        "worst_score": worst_score,
        "best_score": best_score,
        "worst_crop_position": (worst_top, worst_left),
        "num_crops": len(crops),
        "per_crop_scores": scores_pct,
    }


def interpret_score(score: float) -> str:
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
    parser = argparse.ArgumentParser(description="Blur Score Inference (worst-region focused)")
    parser.add_argument("--images", nargs="+", default=None, help="Image paths to analyze.")
    parser.add_argument("--model", default=MODEL_PATH, help="Path to trained model weights.")
    parser.add_argument("--debug", action="store_true", help="Print per-crop scores and positions.")
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
            result = predict_blur_score(model, path, debug=args.debug)
            label = interpret_score(result["overall_score"])
            print(f"{os.path.basename(path)}")
            print(f"  Overall blur score : {result['overall_score']:.2f}%  ({label})")
            print(f"  Median across crops : {result['median_score']:.2f}%  | "
                  f"std: {result['std_score']:.2f}  (high std = uneven blur across frame)")
            print(f"  Range: best={result['best_score']:.2f}% .. worst={result['worst_score']:.2f}% "
                  f"(worst region at top={result['worst_crop_position'][0]}, "
                  f"left={result['worst_crop_position'][1]})")
            print(f"  Crops analyzed: {result['num_crops']}")
        except Exception as exc:
            print(f"Error while processing {path}: {exc}")
        print("-" * 60)


if __name__ == "__main__":
    main()