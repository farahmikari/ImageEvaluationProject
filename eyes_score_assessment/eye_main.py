import os
import cv2

from eyes_score_assessment.face_pipeline import FaceMeshDetector, NoFaceDetectedError
from eyes_score_assessment.ear_calculator import (
    analyze_eye,
    average_ear,
    calculate_image_score,
    describe_image_score,
)


SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


def load_image(image_path: str):
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(
            f"can't read image : {image_path}"
        )

    return image


def print_result(label: str, ear_value: float, percentage: float):
    print(f"{label}:")
    print(f"  EAR = {ear_value:.4f}")
    print(f"eye opening percentage = {percentage:.2f}%")
    print("-" * 40)


def run(image_path: str):
    image = load_image(image_path)
    detector = FaceMeshDetector()
    try:
        all_faces_eyes = detector.detect_eyes(image)

        print("=" * 50)
        print(f"the image: {os.path.basename(image_path)}")
        print(f"faces detected: {len(all_faces_eyes)}")
        print("=" * 50)

        per_face_overall_results = []

        for face_index, (left_eye, right_eye) in enumerate(all_faces_eyes, start=1):
            left_result = analyze_eye(left_eye)
            right_result = analyze_eye(right_eye)
            overall_result = average_ear(left_result, right_result)
            per_face_overall_results.append(overall_result)

            print(f"--- face {face_index} ---")

            print_result(
                "left eye",
                left_result.ear_value,
                left_result.openness_percentage,
            )

            print_result(
                "right eye",
                right_result.ear_value,
                right_result.openness_percentage,
            )

            print_result(
                "average for left and right",
                overall_result.ear_value,
                overall_result.openness_percentage,
            )

        image_score = calculate_image_score(per_face_overall_results)
        score_label = describe_image_score(image_score.openness_percentage)

        print("=" * 50)
        print("FINAL IMAGE SCORE (all faces combined)")
        print(f"  EAR = {image_score.ear_value:.4f}")
        print(f"  eye opening percentage = {image_score.openness_percentage:.2f}%")
        print(f"  rating = {score_label}")
        print("=" * 50)
        print()

    except NoFaceDetectedError:
        print(f"{os.path.basename(image_path)} : can't detect face")

    finally:
        detector.close()


if __name__ == "__main__":

    current_dir = os.path.dirname(os.path.abspath(__file__))

    test_images_dir = os.path.join(current_dir, "test_images")

    if not os.path.exists(test_images_dir):
        print("folder test_images not found")
        exit()

    image_files = [
        os.path.join(test_images_dir, file)
        for file in os.listdir(test_images_dir)
        if file.lower().endswith(SUPPORTED_EXTENSIONS)
    ]

    if not image_files:
        print("there is no images inside test_images folder.")
        exit()

    print(f" {len(image_files)} images found .\n")

    for image_path in image_files:
        run(image_path)
