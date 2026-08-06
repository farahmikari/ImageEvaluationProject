import numpy as np
from config import *
from fusion import compute_all_persons_final_scores
from person_extraction import extract_valid_persons

def compute_person_weight(person_record, size_weight_power=1.0,min_valid_points_ref=17):
    size_factor = person_record["box_to_frame_ratio"] ** size_weight_power
    confidence_factor = person_record["valid_points_count"] / min_valid_points_ref
    confidence_factor = min(1.0, confidence_factor)  
    weight = (size_factor * 0.7) + (confidence_factor * 0.3)
    return weight

def compute_score_dispersion(scores):
    if len(scores) <= 1:
        return 0.0
    return float(np.std(scores))

def filter_background_persons(persons, min_occupancy=MIN_OCCUPANCY_FOR_MAIN_SUBJECT):
    main_subjects = [p for p in persons if p["box_to_frame_ratio"] >= min_occupancy]
    return main_subjects if len(main_subjects) > 0 else persons


def aggregate_person_scores(person_records, dispersion_threshold=DISPERSION_THRESHOLD, 
                              dispersion_penalty_factor=DISPERSION_PENALTY_FACTOR):
    if len(person_records) == 0:
        return None, {"reason": "no_valid_persons"}
    
    confident_persons = [p for p in person_records if p.get("person_final_score") is not None]
    if len(confident_persons) == 0:
        return None, {"reason": "all_persons_invalid_geometric_data"}
    confident_persons = filter_background_persons(confident_persons)    
    scores = [p["person_final_score"] for p in confident_persons]
    weights = [compute_person_weight(p) for p in confident_persons]
    total_weight = sum(weights)
    if total_weight == 0:
        weighted_score = np.mean(scores)
    else:
        weighted_score = sum(s * w for s, w in zip(scores, weights)) / total_weight
    dispersion = compute_score_dispersion(scores)

    if dispersion > dispersion_threshold:
        penalty = (dispersion - dispersion_threshold) * dispersion_penalty_factor
        weighted_score = max(0, weighted_score - penalty)
    
    final_score = round(weighted_score, 1)
    
    details = {
        "num_persons": len(person_records),
        "num_persons_confident": len(confident_persons),  # مفيد لمعرفة كم شخص استُبعد
        "individual_scores": scores,
        "individual_weights": [round(w, 3) for w in weights],
        "dispersion": round(dispersion, 2),
        "penalty_applied": dispersion > dispersion_threshold,
    }
    return final_score, details

def get_image_pose_score(image_path):
    person_records = extract_valid_persons(image_path)
    if len(person_records) == 0:
        return None, {"reason": "no_valid_persons_detected"}
    person_records = compute_all_persons_final_scores(person_records)
    final_score, details = aggregate_person_scores(person_records)
    return final_score, details
        