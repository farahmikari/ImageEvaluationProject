import os
import logging
import warnings
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
logging.getLogger("transformers").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")
from transformers import AutoProcessor, AutoModel
import transformers
transformers.logging.set_verbosity_error()
import torch
import numpy as np
from person_extraction import *
from config import *


device = "cuda" if torch.cuda.is_available() else "cpu"

MODEL_NAME = SIGLIP_MODEL_NAME

model = AutoModel.from_pretrained(MODEL_NAME).to(device)
processor = AutoProcessor.from_pretrained(MODEL_NAME)
model.eval()

def compute_siglip_score_single(crop_image, prompt_pairs=PROMPT_PAIRS):
    all_texts = []
    for pair in prompt_pairs:
        all_texts.append(pair["positive"])
        all_texts.append(pair["negative"])
    
    inputs = processor(
        text=all_texts,
        images=crop_image,
        padding="max_length",
        return_tensors="pt"
    ).to(device)
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits_per_image[0] 
        probs = torch.sigmoid(logits).cpu().numpy()
    pair_scores = []
    pair_details = []
    
    for i, pair in enumerate(prompt_pairs):
        pos_prob = probs[i * 2]
        neg_prob = probs[i * 2 + 1]
        
        pair_score = pos_prob / (pos_prob + neg_prob + 1e-8)
        
        pair_scores.append(pair_score * pair["weight"])
        pair_details.append({
            "positive_text": pair["positive"],
            "pos_prob": float(pos_prob),
            "neg_prob": float(neg_prob),
            "pair_score": float(pair_score),
        })
    
    total_weight = sum(p["weight"] for p in prompt_pairs)
    final_score = sum(pair_scores) / total_weight
    
    return final_score, pair_details

def calibrate_siglip_score(raw_score, min_observed=SIGLIP_CALIBRATION_MIN, max_observed=SIGLIP_CALIBRATION_MAX,softness=SIGLIP_CALIBRATION_SOFTNESS):
    soft_min = min_observed - softness
    soft_max = max_observed + softness
    
    clipped = max(soft_min, min(raw_score, soft_max))
    normalized = (clipped - soft_min) / (soft_max - soft_min)
    return max(0, min(1, normalized))


def compute_siglip_scores_batch(crop_images, prompt_pairs=PROMPT_PAIRS,apply_calibration=True):
    if len(crop_images) == 0:
        return []
    
    all_texts = []
    for pair in prompt_pairs:
        all_texts.append(pair["positive"])
        all_texts.append(pair["negative"])
    inputs = processor(
        text=all_texts,
        images=crop_images,
        padding="max_length",
        return_tensors="pt"
    ).to(device)
    
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits_per_image.cpu().numpy()  
            
    
    results = []
    for img_idx in range(len(crop_images)):
        pair_scores = []
        pair_details = []
        
        for i, pair in enumerate(prompt_pairs):
            pos_logit = logits[img_idx, i * 2]
            neg_logit = logits[img_idx, i * 2 + 1]
            logit_diff = pos_logit - neg_logit
            pair_score = 1 / (1 + np.exp(-logit_diff))
            
            pair_scores.append(pair_score * pair["weight"])
            pair_details.append({
                "positive_text": pair["positive"],
                "pos_prob": float(pos_logit),
                "neg_prob": float(neg_logit),
                "logit_diff": float(logit_diff),
                "pair_score": float(pair_score),
            })
        
        total_weight = sum(p["weight"] for p in prompt_pairs)
        final_score = sum(pair_scores) / total_weight
        if apply_calibration:
            final_score=calibrate_siglip_score(final_score)
        results.append((final_score, pair_details))
    
    return results

def add_siglip_scores_to_persons(person_records, prompt_pairs=PROMPT_PAIRS):
    if len(person_records) == 0:
        return person_records
    
    crop_images = [p["crop_image"] for p in person_records]
    results = compute_siglip_scores_batch(crop_images, prompt_pairs)
    
    for person, (score, details) in zip(person_records, results):
        person["siglip_score"] = score
        person["siglip_details"] = details
    
    return person_records 