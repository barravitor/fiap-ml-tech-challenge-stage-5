# training/pipeline/feature_engineering.py
from datetime import datetime

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from shared.utils.preprocessing import preprocess_text

model = SentenceTransformer("all-MiniLM-L6-v2")

def concat_fields(*fields):
    return ' '.join(str(f).strip() for f in fields if f)

def calculate_similarity(candidate_text: str, job_text: str):
    candidate_embed = model.encode(candidate_text, convert_to_tensor=True)
    job_embed = model.encode(job_text, convert_to_tensor=True)
    return float(util.pytorch_cos_sim(candidate_embed, job_embed))

def get_age(date_of_birth: str) -> int :
    if not date_of_birth or not isinstance(date_of_birth, str):
        return 0

    try:
        birth_date = datetime.strptime(date_of_birth, "%d-%m-%Y")
    except ValueError:
        return 0

    today = datetime.today()
    age = today.year - birth_date.year

    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1

    return age

def get_language_level(language_level: str) -> int:
    if not language_level or not isinstance(language_level, str):
        return 0

    valid_levels = ["fluente", "avancado", "intermediario", "basico"]
    return int(any(level in language_level for level in valid_levels))

def get_language_text(language_name: str, language_level: str) -> str:
    if not language_level or not isinstance(language_level, str):
        return ''

    valid_levels = ["fluente", "avancado", "intermediario", "basico"]
    lol = int(any(level in language_level for level in valid_levels))

    if lol == 0:
        return ''

    return language_name

def score_of_the_match_between_two_texts(fist_text: str, second_text: str):
    first_tokens = set(preprocess_text(str(fist_text or '')))
    second_tokens = set(preprocess_text(str(second_text or '')))

    if len(first_tokens) == 0 or len(second_tokens) == 0:
        return 0
    
    common_tokens = first_tokens.intersection(second_tokens)

    return len(common_tokens) / len(first_tokens)

def process_features(document: dict):
    concat_user_fields = concat_fields(
        document.get('user_professional_title'),
        document.get('user_cv'),
        document.get('user_courses'),
        document.get('user_skills'),
        document.get('user_areas_of_activity')
    )

    return {
        "score_job_title": score_of_the_match_between_two_texts(
            document.get('job_title'),
            concat_user_fields
        ),
        "score_job_skills": score_of_the_match_between_two_texts(
            document.get('job_skills'),
            concat_fields(
                document.get('user_professional_title'),
                document.get('user_cv'),
                document.get('user_courses'),
                document.get('user_skills')
            )
        ),
        "score_job_location": score_of_the_match_between_two_texts(
            document.get('job_local'),
            concat_fields(
                document.get('user_local'),
                document.get('user_cv')
            )
        ),
        "score_job_areas_of_activity": score_of_the_match_between_two_texts(
            document.get('job_areas_of_activity'),
            concat_user_fields
        ),
        "score_job_activities": score_of_the_match_between_two_texts(
            document.get('job_activities'),
            concat_user_fields
        ),
        "score_job_language_english": score_of_the_match_between_two_texts(
            get_language_text('ingles', document["user_language_english_level"]),
            concat_fields(
                document.get('job_skills'),
                document.get('job_areas_of_activity'),
                document.get('job_activities')
            )
        ),
        # "score_job_language_spanish": score_of_the_match_between_two_texts(
        #     get_language_text('espanhol', document["user_language_spanish_level"]),
        #     concat_fields(
        #         document.get('job_skills'),
        #         document.get('job_areas_of_activity'),
        #         document.get('job_activities')
        #     )
        # ),
        "score_job_academic_level": score_of_the_match_between_two_texts(
            document["user_academic_level"],
            concat_fields(
                document.get('job_skills'),
                document.get('job_areas_of_activity'),
                document.get('job_activities')
            )
        ),

        # User informations
        # "user_language_english": get_language_level(document["user_language_english_level"]),
        # "user_language_spanish": get_language_level(document["user_language_spanish_level"]),
        # "user_language_other": get_language_level(document["user_language_other_level"]),
        # "user_date_of_birth": get_age(document["user_date_of_birth"]),
        # "user_higher_education": int("superior" in str(document.get('user_academic_level'))),
        # "user_high_school": int("medio" in str(document.get('user_academic_level'))),
        # "user_postgraduate_studies": int("pos" in str(document.get('user_academic_level'))),
        # "user_technical_education": int("tecnico" in str(document.get('user_academic_level'))),

        # Job informations
        # "job_language_english": get_language_level(document["job_language_english_level"]),
        # "job_language_spanish": get_language_level(document["job_language_spanish_level"]),
        # "job_language_other": get_language_level(document["job_language_other_level"]),
        # "job_higher_education": int("superior" in str(document.get('job_academic_level'))),
        # "job_high_school": int("medio" in str(document.get('job_academic_level'))),
        # "job_postgraduate_studies": int("pos" in str(document.get('job_academic_level'))),
        # "job_technical_education": int("tecnico" in str(document.get('job_academic_level'))),
    }