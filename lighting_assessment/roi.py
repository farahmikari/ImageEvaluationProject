import cv2
import numpy as np


FACE_OVAL_LANDMARKS = [
    10, 338, 297, 332, 284, 251, 389, 356,
    454, 323, 361, 288, 397, 365, 379, 378,
    400, 377, 152, 148, 176, 149, 150, 136,
    172, 58, 132, 93, 234, 127, 162, 21,
    54, 103, 67, 109
]

LEFT_EYE_LANDMARKS = [
    33, 246, 161, 160, 159, 158, 157, 173,
    133, 155, 154, 153, 145, 144, 163, 7
]

RIGHT_EYE_LANDMARKS = [
    362, 398, 384, 385, 386, 387, 388, 466,
    263, 249, 390, 373, 374, 380, 381, 382
]

LIPS_LANDMARKS = [
    61, 185, 40, 39, 37, 0, 267, 269, 270,
    409, 291, 375, 321, 405, 314, 17, 84,
    181, 91, 146
]


def landmarks_to_points(face_landmarks, indices, width, height):
    points = []

    for index in indices:
        landmark = face_landmarks.landmark[index]
        x = int(landmark.x * width)
        y = int(landmark.y * height)
        points.append([x, y])

    return np.array(points, dtype=np.int32)


def create_face_skin_mask(image, face_landmarks):
    height, width = image.shape[:2]

    mask = np.zeros((height, width), dtype=np.uint8)

    face_points = landmarks_to_points(
        face_landmarks,
        FACE_OVAL_LANDMARKS,
        width,
        height,
    )

    cv2.fillPoly(mask, [face_points], 255)

    left_eye_points = landmarks_to_points(
        face_landmarks,
        LEFT_EYE_LANDMARKS,
        width,
        height,
    )

    right_eye_points = landmarks_to_points(
        face_landmarks,
        RIGHT_EYE_LANDMARKS,
        width,
        height,
    )

    lips_points = landmarks_to_points(
        face_landmarks,
        LIPS_LANDMARKS,
        width,
        height,
    )

    cv2.fillPoly(mask, [left_eye_points], 0)
    cv2.fillPoly(mask, [right_eye_points], 0)
    cv2.fillPoly(mask, [lips_points], 0)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.GaussianBlur(mask, (7, 7), 0)

    return mask


def create_masked_preview(image, mask):
    preview = image.copy()
    preview[mask == 0] = 0
    return preview