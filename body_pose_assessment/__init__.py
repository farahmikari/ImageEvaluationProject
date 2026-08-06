# __init__.py
from person_extraction import extract_valid_persons
from fusion import compute_all_persons_final_scores
from aggregation import aggregate_person_scores


def assess_pose_aesthetic(image_path):
    try:
        person_records = extract_valid_persons(image_path)
        
        if len(person_records) == 0:
            return {"score": None, "status": "no_person_detected", "details": None}
        
        person_records = compute_all_persons_final_scores(person_records)
        final_score, details = aggregate_person_scores(person_records)
        
        if final_score is None:
            return {"score": None, "status": "no_valid_geometric_data", "details": details}
        
        return {"score": final_score, "status": "success", "details": details}
    
    except Exception as e:
        return {"score": None, "status": "error", "details": {"error_message": str(e)}}