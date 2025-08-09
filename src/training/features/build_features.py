from training.embedding.embed_text import cosine_sim
from training.preprocessing.text import treat_missing
from shared.config import STATUS_MAP

def map_candidate_status(status: str) -> int:
    if not isinstance(status, str):
        return 0

    for key, value in STATUS_MAP.items():
        if key.lower() in status.lower():
            return value

    return 0

def process_features(document: dict):
    features = {
        'same_state': [int(treat_missing(document.get('user_local_state'), "[missing_user_local_state]") == treat_missing(document.get('job_local_state'), "[missing_job_local_state]"))],
        'same_academic_level': [int(treat_missing(document.get('user_academic_level'), "[missing_user_academic_level]") == treat_missing(document.get('job_academic_level'), "[missing_job_academic_level]"))],

        'distance_km': [document.get('distance_km')],
        'job_areas_of_activity': document.get('job_areas_of_activity_embed'),
        'user_areas_of_activity': document.get('user_areas_of_activity_embed'),
        'sim_areas_of_activity': [cosine_sim(document.get('user_areas_of_activity_embed'), document.get('job_areas_of_activity_embed'))],
        'job_resume': document.get('job_resume_embed'),
        'user_resume': document.get('user_resume_embed'),
        'sim_resume': [cosine_sim(document.get('user_resume_embed'), document.get('job_resume_embed'))],
        'target': map_candidate_status(document.get('candidate_status', ''))
    }

    return features
