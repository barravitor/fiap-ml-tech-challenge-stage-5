# training/pipeline/feature_engineering.py
from datetime import datetime

import numpy as np
from sentence_transformers import SentenceTransformer
from shared.utils.preprocessing import preprocess_text

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def concat_fields(*fields):
    return ' '.join(str(f).strip() for f in fields if f)

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

def map_candidate_status(status: str) -> int:
    STATUS_MAP = {
        # Negative statuses
        'Inscrito': 0,
        'Desistiu': 0,
        'Desistiu da Contratação': 0,
        'Não Aprovado pelo Cliente': 0,
        'Não Aprovado pelo RH': 0,
        'Não Aprovado pelo Requisitante': 0,
        'Recusado': 0,
        'Sem interesse nesta vaga': 0,
        # Intermediate statuses
        'Em avaliação pelo RH': 0,
        'Encaminhado ao Requisitante': 1,
        'Entrevista Técnica': 1,
        'Entrevista com Cliente': 1,
        'Encaminhar Proposta': 1,
        'Documentação CLT': 1,
        'Documentação Cooperado': 1,
        'Documentação PJ': 1,
        # Success status
        'Aprovado': 1,
        'Contratado como Hunting': 1,
        'Contratado pela Decision': 1,
        'Proposta Aceita': 1,
    }

    if not isinstance(status, str):
        return 0

    for key, value in STATUS_MAP.items():
        if key.lower() in status.lower():
            return value

    return 0

def process_features(document: dict):
    target = map_candidate_status(document.get('candidate_status', ''))

    concat_user_fields = concat_fields(
        document.get('user_professional_title'),
        document.get('user_cv'),
        document.get('user_courses'),
        document.get('user_skills'),
        document.get('user_areas_of_activity')
    )

    concat_job_fields = concat_fields(
        document.get('job_title'),
        document.get('job_skills'),
        document.get('job_local'),
        document.get('job_areas_of_activity'),
        document.get('job_activities')
    )

    job_embed = model.encode(concat_job_fields)
    user_embed = model.encode(concat_user_fields)

    # features = {
    #     "job_embed_cv_embed": np.hstack((job_embed, user_embed))
    #     # "score_job_title": score_of_the_match_between_two_texts(
    #     #     document.get('job_title'),
    #     #     concat_user_fields
    #     # ),
    #     # "score_job_skills": score_of_the_match_between_two_texts(
    #     #     document.get('job_skills'),
    #     #     concat_fields(
    #     #         document.get('user_professional_title'),
    #     #         document.get('user_cv'),
    #     #         document.get('user_courses'),
    #     #         document.get('user_skills')
    #     #     )
    #     # ),
    #     # "score_job_location": score_of_the_match_between_two_texts(
    #     #     document.get('job_local'),
    #     #     concat_fields(
    #     #         document.get('user_local'),
    #     #         document.get('user_cv')
    #     #     )
    #     # ),
    #     # "score_job_areas_of_activity": score_of_the_match_between_two_texts(
    #     #     document.get('job_areas_of_activity'),
    #     #     concat_user_fields
    #     # ),
    #     # "score_job_activities": score_of_the_match_between_two_texts(
    #     #     document.get('job_activities'),
    #     #     concat_user_fields
    #     # ),
    #     # "score_job_language_english": score_of_the_match_between_two_texts(
    #     #     get_language_text('ingles', document["user_language_english_level"]),
    #     #     concat_fields(
    #     #         document.get('job_skills'),
    #     #         document.get('job_areas_of_activity'),
    #     #         document.get('job_activities')
    #     #     )
    #     # ),
    #     # # "score_job_language_spanish": score_of_the_match_between_two_texts(
    #     # #     get_language_text('espanhol', document["user_language_spanish_level"]),
    #     # #     concat_fields(
    #     # #         document.get('job_skills'),
    #     # #         document.get('job_areas_of_activity'),
    #     # #         document.get('job_activities')
    #     # #     )
    #     # # ),
    #     # "score_job_academic_level": score_of_the_match_between_two_texts(
    #     #     document["user_academic_level"],
    #     #     concat_fields(
    #     #         document.get('job_skills'),
    #     #         document.get('job_areas_of_activity'),
    #     #         document.get('job_activities')
    #     #     )
    #     # ),

    #     # # User informations
    #     # "user_language_english": get_language_level(document["user_language_english_level"]),
    #     # # "user_language_spanish": get_language_level(document["user_language_spanish_level"]),
    #     # # "user_language_other": get_language_level(document["user_language_other_level"]),
    #     # # "user_date_of_birth": get_age(document["user_date_of_birth"]),
    #     # "user_higher_education": int("superior" in str(document.get('user_academic_level'))),
    #     # # "user_high_school": int("medio" in str(document.get('user_academic_level'))),
    #     # # "user_postgraduate_studies": int("pos" in str(document.get('user_academic_level'))),
    #     # # "user_technical_education": int("tecnico" in str(document.get('user_academic_level'))),

    #     # # Job informations
    #     # "job_language_english": get_language_level(document["job_language_english_level"]),
    #     # # "job_language_spanish": get_language_level(document["job_language_spanish_level"]),
    #     # # "job_language_other": get_language_level(document["job_language_other_level"]),
    #     # "job_higher_education": int("superior" in str(document.get('job_academic_level'))),
    #     # # "job_high_school": int("medio" in str(document.get('job_academic_level'))),
    #     # # "job_postgraduate_studies": int("pos" in str(document.get('job_academic_level'))),
    #     # # "job_technical_education": int("tecnico" in str(document.get('job_academic_level'))),
    # }

    return np.hstack((job_embed, user_embed)), target