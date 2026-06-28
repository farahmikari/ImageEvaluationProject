import cv2
import numpy as np


def get_luminance_channel(image):
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    return ycrcb[:, :, 0]


def get_valid_pixels(y_channel, mask=None):
    if mask is None:
        return y_channel.reshape(-1)

    valid_pixels = y_channel[mask > 0]

    if valid_pixels.size == 0:
        return None

    return valid_pixels


def calculate_mean_luminance(image, mask=None):
    y_channel = get_luminance_channel(image)
    pixels = get_valid_pixels(y_channel, mask)

    if pixels is None:
        return None

    return float(np.mean(pixels))


def calculate_shadow_clipping_ratio(image, mask=None, threshold=15):
    y_channel = get_luminance_channel(image)
    pixels = get_valid_pixels(y_channel, mask)

    if pixels is None:
        return None

    shadow_pixels = np.sum(pixels <= threshold)
    return float(shadow_pixels / pixels.size)


def calculate_highlight_clipping_ratio(image, mask=None, threshold=245):
    y_channel = get_luminance_channel(image)
    pixels = get_valid_pixels(y_channel, mask)

    if pixels is None:
        return None

    highlight_pixels = np.sum(pixels >= threshold)
    return float(highlight_pixels / pixels.size)


def calculate_well_exposedness_score(image, mask=None, sigma=0.25):
    y_channel = get_luminance_channel(image).astype(np.float32) / 255.0

    if mask is not None:
        pixels = y_channel[mask > 0]
    else:
        pixels = y_channel.reshape(-1)

    if pixels.size == 0:
        return None

    well_exposedness = np.exp(-((pixels - 0.5) ** 2) / (2 * sigma ** 2))
    return float(np.mean(well_exposedness) * 100)


def calculate_entropy(image, mask=None):
    y_channel = get_luminance_channel(image)
    pixels = get_valid_pixels(y_channel, mask)

    if pixels is None:
        return None

    histogram = cv2.calcHist(
        [pixels.astype(np.uint8)],
        [0],
        None,
        [256],
        [0, 256],
    )

    histogram = histogram / np.sum(histogram)
    histogram = histogram[histogram > 0]

    entropy = -np.sum(histogram * np.log2(histogram))
    return float(entropy)


def calculate_uniformity(image, mask=None, grid_size=4):
    y_channel = get_luminance_channel(image)
    height, width = y_channel.shape

    block_height = height // grid_size
    block_width = width // grid_size

    block_values = []

    for row in range(grid_size):
        for col in range(grid_size):
            y1 = row * block_height
            y2 = (row + 1) * block_height
            x1 = col * block_width
            x2 = (col + 1) * block_width

            block = y_channel[y1:y2, x1:x2]

            if mask is not None:
                mask_block = mask[y1:y2, x1:x2]
                block_pixels = block[mask_block > 0]

                if block_pixels.size == 0:
                    continue

                block_values.append(np.mean(block_pixels))
            else:
                block_values.append(np.mean(block))

    if len(block_values) < 2:
        return None

    std_value = np.std(np.array(block_values))

    uniformity = 1 - (std_value / 128)
    uniformity = max(0, min(1, uniformity))

    return float(uniformity)


def extract_lighting_metrics(image, mask=None):
    return {
        "mean_luminance": calculate_mean_luminance(image, mask),
        "shadow_clipping_ratio": calculate_shadow_clipping_ratio(image, mask),
        "highlight_clipping_ratio": calculate_highlight_clipping_ratio(image, mask),
        "well_exposedness_score": calculate_well_exposedness_score(image, mask),
        "entropy": calculate_entropy(image, mask),
        "uniformity": calculate_uniformity(image, mask),
    }