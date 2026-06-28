def clamp(value, min_value=0.0, max_value=100.0):
    return max(min_value, min(max_value, value))


def weighted_average(scores_with_weights):
    total_score = 0.0
    total_weight = 0.0

    for score, weight in scores_with_weights:
        if score is None:
            continue

        total_score += score * weight
        total_weight += weight

    if total_weight == 0:
        return None

    return total_score / total_weight


def score_mean_luminance(mean_luminance):
    if mean_luminance is None:
        return None

    value = mean_luminance

    if value <= 30:
        score = (value / 30.0) * 25.0

    elif value <= 70:
        score = 25.0 + ((value - 30.0) / 40.0) * 35.0

    elif value <= 180:
        score = 60.0 + ((value - 70.0) / 110.0) * 40.0

    elif value <= 220:
        score = 100.0 - ((value - 180.0) / 40.0) * 25.0

    else:
        score = 75.0 - ((value - 220.0) / 35.0) * 75.0

    return round(clamp(score), 2)


def score_shadow_clipping(shadow_ratio):
    if shadow_ratio is None:
        return None

    if shadow_ratio <= 0.03:
        return 100.0

    if shadow_ratio >= 0.45:
        return 0.0

    score = 100.0 - ((shadow_ratio - 0.03) / (0.45 - 0.03)) * 100.0
    return round(clamp(score), 2)


def score_highlight_clipping(highlight_ratio):
    if highlight_ratio is None:
        return None

    if highlight_ratio <= 0.02:
        return 100.0

    if highlight_ratio >= 0.25:
        return 0.0

    score = 100.0 - ((highlight_ratio - 0.02) / (0.25 - 0.02)) * 100.0
    return round(clamp(score), 2)


def score_well_exposedness(well_exposedness_score):
    if well_exposedness_score is None:
        return None

    return round(clamp(well_exposedness_score), 2)


def score_entropy(entropy):
    if entropy is None:
        return None

    if entropy <= 5.5:
        return 40.0

    if entropy >= 7.5:
        return 100.0

    score = 40.0 + ((entropy - 5.5) / (7.5 - 5.5)) * 60.0
    return round(clamp(score), 2)


def score_uniformity(uniformity):
    if uniformity is None:
        return None

    if uniformity <= 0.30:
        return 0.0

    if uniformity >= 0.85:
        return 100.0

    score = ((uniformity - 0.30) / (0.85 - 0.30)) * 100.0
    return round(clamp(score), 2)


def normalize_metric_scores(metrics):
    return {
        "mean_luminance_score": score_mean_luminance(
            metrics.get("mean_luminance")
        ),
        "shadow_clipping_score": score_shadow_clipping(
            metrics.get("shadow_clipping_ratio")
        ),
        "highlight_clipping_score": score_highlight_clipping(
            metrics.get("highlight_clipping_ratio")
        ),
        "well_exposedness_score_normalized": score_well_exposedness(
            metrics.get("well_exposedness_score")
        ),
        "entropy_score": score_entropy(
            metrics.get("entropy")
        ),
        "uniformity_score": score_uniformity(
            metrics.get("uniformity")
        ),
    }


def calculate_region_lighting_score(metrics):
    metric_scores = normalize_metric_scores(metrics)

    region_score = weighted_average([
        (metric_scores["well_exposedness_score_normalized"], 0.40),
        (metric_scores["mean_luminance_score"], 0.20),
        (metric_scores["shadow_clipping_score"], 0.15),
        (metric_scores["highlight_clipping_score"], 0.10),
        (metric_scores["uniformity_score"], 0.10),
        (metric_scores["entropy_score"], 0.05),
    ])

    return {
        "metric_scores": metric_scores,
        "lighting_score": round(region_score, 2) if region_score is not None else None,
    }


def calculate_final_lighting_score(roi_metrics):
    region_scores = {}

    for roi_name, metrics in roi_metrics.items():
        region_scores[roi_name] = calculate_region_lighting_score(metrics)

    whole_score = region_scores.get("whole_image", {}).get("lighting_score")

    face_skin_score = None
    if "face_skin" in region_scores:
        face_skin_score = region_scores["face_skin"]["lighting_score"]

    if face_skin_score is None:
        final_score = whole_score
    else:
        final_score = weighted_average([
            (whole_score, 0.45),
            (face_skin_score, 0.55),
        ])

    return {
        "region_scores": region_scores,
        "final_lighting_score": round(final_score, 2) if final_score is not None else None,
    }