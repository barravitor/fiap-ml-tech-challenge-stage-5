from typing import List
from shared.utils.preprocessing import normalize_text

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
        'Em avaliação pelo RH': 1,
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

def extract_job_info(job_id: int, job_dict: dict):
    return {
        'job_id': job_id,
        'title': normalize_text(job_dict['informacoes_basicas']['titulo_vaga']),
        'local': normalize_text(f"{job_dict['perfil_vaga']['estado']} {job_dict['perfil_vaga']['cidade']}"),
        'type_of_hire': normalize_text(job_dict['informacoes_basicas']['tipo_contratacao']),
        'academic_level': normalize_text(job_dict['perfil_vaga']['nivel_academico']),
        'language_english_level': normalize_text(job_dict['perfil_vaga']['nivel_ingles']),
        'language_spanish_level': normalize_text(job_dict['perfil_vaga']['nivel_espanhol']),
        'language_other_level': normalize_text(job_dict['perfil_vaga']['outro_idioma']),
        'areas_of_activity': normalize_text(job_dict['perfil_vaga']['areas_atuacao']),
        'activities': normalize_text(job_dict['perfil_vaga']['principais_atividades']),
        'skills': normalize_text(job_dict['perfil_vaga']['competencia_tecnicas_e_comportamentais'])
    }

def extract_user_info(user_id: int, user_dict: dict):
    return {
        'user_id': user_id,
        'professional_objective': normalize_text(user_dict['infos_basicas']['objetivo_profissional']),
        'professional_title': normalize_text(user_dict['informacoes_profissionais']['titulo_profissional']),
        'language_english_level': normalize_text(user_dict['formacao_e_idiomas']['nivel_ingles']),
        'language_spanish_level': normalize_text(user_dict['formacao_e_idiomas']['nivel_espanhol']),
        'language_other_level': normalize_text(user_dict['formacao_e_idiomas']['outro_idioma']),
        'date_of_birth': user_dict['informacoes_pessoais']['data_nascimento'],
        'name': normalize_text(user_dict['informacoes_pessoais']['nome']),
        'local': normalize_text(user_dict.get('informacoes_pessoais', {}).get('endereco') or user_dict.get('infos_basicas', {}).get('local')),
        'academic_level': normalize_text(user_dict['formacao_e_idiomas']['nivel_academico']),
        'cv': normalize_text(user_dict.get('cv_pt', '')),
        'skills': normalize_text(user_dict.get('informacoes_profissionais', {}).get('conhecimentos_tecnicos')),
        'areas_of_activity': normalize_text(user_dict.get('informacoes_profissionais', {}).get('area_atuacao')),
        'courses': normalize_text(user_dict.get('formacao_e_idiomas', {}).get('cursos')),
    }

def extract_job_candidates_info(job_id: int, jobs, users, prospects: List[dict]) -> List :
    job = jobs.get(str(job_id))

    if job is None:
        print(f"Job not found: ID {job_id}.")
        return []

    extract_job = extract_job_info(job_id, job)

    print(f"Job: {extract_job['title']}")
    
    rows = []
    for prospect in prospects:
        user_id = prospect.get('codigo')
        user = users.get(str(user_id))

        if user is None:
            print(f"User not found: ID {user_id}.")
            continue

        extract_user = extract_user_info(user_id, user)

        rows.append({
            'job_id': job_id,
            'user_id': user_id,

            # User informations
            'user_skills': extract_user['skills'],
            'user_courses': extract_user['courses'],
            'user_areas_of_activity': extract_user['areas_of_activity'],
            'user_cv': extract_user['cv'],
            'user_professional_objective': extract_user['professional_objective'],
            'user_professional_title': extract_user['professional_title'],
            'user_language_english_level': extract_user['language_english_level'],
            'user_language_spanish_level': extract_user['language_spanish_level'],
            'user_language_other_level': extract_user['language_other_level'],
            'user_date_of_birth': extract_user['date_of_birth'],
            'user_local': extract_user['local'],
            'user_academic_level': extract_user['academic_level'],

            # Job informations
            'job_title': extract_job['title'],
            'job_activities': extract_job['activities'],
            'job_skills': extract_job['skills'],
            'job_local': extract_job['local'],
            'job_type_of_hire': extract_job['type_of_hire'],
            'job_language_english_level': extract_job['language_english_level'],
            'job_language_spanish_level': extract_job['language_spanish_level'],
            'job_language_other_level': extract_job['language_other_level'],
            'job_areas_of_activity': extract_job['areas_of_activity'],
            'job_academic_level': extract_job['academic_level'],

            # Candidate informations
            'candidate_status': map_candidate_status(prospect.get('situacao_candidado', ''))
        })

    return rows