import os

import numpy as np
from geometric_score import compute_geometric_score
from person_extraction import extract_valid_persons
from siglip_score import add_siglip_scores_to_persons
from config import *

def compute_disagreement(geo_score, siglip_score):
    return abs(geo_score - siglip_score)

def fuse_scores(geo_score, siglip_score, weights=FUSION_WEIGHTS, 
                 disagreement_threshold=DISAGREEMENT_THRESHOLD, trust_ratio=TRUST_RATIO):
    disagreement = compute_disagreement(geo_score, siglip_score)
    if disagreement <= disagreement_threshold:
        weighted_avg = (geo_score * weights["geometric"] + 
                         siglip_score * weights["siglip"])
        return weighted_avg, disagreement    
    if geo_score > siglip_score:
        resolved_score = geo_score * trust_ratio + siglip_score * (1 - trust_ratio)
    else:
        resolved_score = siglip_score * trust_ratio + geo_score * (1 - trust_ratio)
    
    return resolved_score, disagreement

def calibrate_to_100_scale(raw_score, min_observed=0.15, max_observed=0.90):
    clipped = np.clip(raw_score, min_observed, max_observed)
    normalized = (clipped - min_observed) / (max_observed - min_observed)
    return round(normalized * 100, 1)

def compute_person_final_score(person_record, fusion_weights=FUSION_WEIGHTS):
    geo_result = compute_geometric_score(person_record)
    if geo_result is None:
        person_record["geometric_score"] = None
        person_record["person_final_score"] = None
        person_record["confidence_status"] = "insufficient_geometric_data"
        return person_record
    
    geo_score, _ = geo_result
    person_record["geometric_score"] = geo_score
    raw_score, disagreement = fuse_scores(geo_score, person_record["siglip_score"], fusion_weights)
    person_record["disagreement_level"] = disagreement
    
    person_record["person_final_score"] = calibrate_to_100_scale(raw_score)
    person_record["confidence_status"] = "confident" if disagreement <= DISAGREEMENT_THRESHOLD else "resolved_high_conflict"
    return person_record

def compute_all_persons_final_scores(person_records, fusion_weights=FUSION_WEIGHTS):
    if len(person_records) == 0:
        return person_records    
    person_records = add_siglip_scores_to_persons(person_records)
    for person in person_records:
        compute_person_final_score(person, fusion_weights)
    return person_records
