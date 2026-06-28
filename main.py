import os
import time
import cv2
import pandas as pd

from lighting_assessment.evaluator import LightingEvaluator


IMAGE_FOLDER = "SGLVD_v1"
OUTPUT_FOLDER = "results"
OUTPUT_FILE = "lighting_scores_detailed_results.csv"

SUPPORTED_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff",
)


def flatten_roi_metrics(roi_metrics):
    flat = {}

    for roi_name, metrics in roi_metrics.items():
        for metric_name, value in metrics.items():
            flat[f"{roi_name}_{metric_name}"] = value

    return flat


def flatten_region_scores(region_scores):
    flat = {}

    for roi_name, score_data in region_scores.items():
        metric_scores = score_data["metric_scores"]

        for score_name, value in metric_scores.items():
            flat[f"{roi_name}_{score_name}"] = value

        flat[f"{roi_name}_lighting_score"] = score_data["lighting_score"]

    return flat


def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    evaluator = LightingEvaluator()
    rows = []

    image_files = sorted([
        file for file in os.listdir(IMAGE_FOLDER)
        if file.lower().endswith(SUPPORTED_EXTENSIONS)
    ])

    print(f"Found {len(image_files)} images.\n")

    for image_name in image_files:
        image_path = os.path.join(IMAGE_FOLDER, image_name)
        image = cv2.imread(image_path)

        if image is None:
            print(f"Cannot read {image_name}")
            continue

        start = time.perf_counter()

        evaluation = evaluator.evaluate_image(image)

        elapsed_ms = (time.perf_counter() - start) * 1000
        height, width = image.shape[:2]

        roi_metrics = evaluation["roi_metrics"]
        region_scores = evaluation["region_scores"]
        final_lighting_score = evaluation["final_lighting_score"]

        row = {
            "Image": image_name,
            "Width": width,
            "Height": height,
            "Detected_ROIs": ",".join(roi_metrics.keys()),
            **flatten_roi_metrics(roi_metrics),
            **flatten_region_scores(region_scores),
            "final_lighting_score": final_lighting_score,
            "Processing_Time_ms": round(elapsed_ms, 2),
        }

        rows.append(row)

        print(
            f"Processed {image_name}: "
            f"{row['Detected_ROIs']} | "
            f"Final Score = {final_lighting_score}"
        )

    df = pd.DataFrame(rows)

    output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)
    df.to_csv(output_path, index=False)

    print("\n=================================")
    print("Detailed lighting score evaluation finished.")
    print(f"CSV saved to:\n{output_path}")
    print("=================================")


if __name__ == "__main__":
    main()