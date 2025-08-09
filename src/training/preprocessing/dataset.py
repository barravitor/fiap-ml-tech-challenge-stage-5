from typing import List
from training.preprocessing.text import normalize_text

def extract_job_info(job_id: int, job_dict: dict):
    profile = job_dict.get('perfil_vaga', {})
    basic_info = job_dict.get('informacoes_basicas', {})

    return {
        'job_id': job_id,
        'job_title': normalize_text(basic_info.get('titulo_vaga')),
        'job_local': normalize_text(f"{profile.get('estado')} {profile.get('cidade')}"),
        'job_local_state': normalize_text(profile.get('estado')),
        'job_local_city': normalize_text(profile.get('cidade')),
        'job_type_of_hire': normalize_text(basic_info.get('tipo_contratacao')),
        'job_academic_level': normalize_text(profile.get('nivel_academico')),
        'job_language_english_level': normalize_text(profile.get('nivel_ingles')),
        'job_language_spanish_level': normalize_text(profile.get('nivel_espanhol')),
        'job_language_other_level': normalize_text(profile.get('outro_idioma')),
        'job_areas_of_activity': normalize_text(profile.get('areas_atuacao')),
        'job_activities': normalize_text(profile.get('principais_atividades')),
        'job_professional_level': normalize_text(profile.get('nivel profissional')),
        'job_skills': normalize_text(profile.get('competencia_tecnicas_e_comportamentais')),
        'job_necessary_behavioral_skills': normalize_text(profile.get('habilidades_comportamentais_necessarias')),
    }

def extract_user_info(user_id: int, user_dict: dict):
    language = user_dict.get('formacao_e_idiomas', {})
    professional = user_dict.get('informacoes_profissionais', {})
    personal_information = user_dict.get('informacoes_pessoais', {})
    basic_info = user_dict.get('infos_basicas', {})
    address =  basic_info.get('local')

    return {
        'user_id': user_id,
        'user_local': normalize_text(basic_info.get('local')),
        'user_local_state': normalize_text(personal_information.get('endereco')),
        'user_local_city': normalize_text(address.split(',')[0].strip() if address else ''),
        'user_professional_objective': normalize_text(basic_info.get('objetivo_profissional')),
        'user_professional_title': normalize_text(professional.get('titulo_profissional')),
        'user_language_english_level': normalize_text(language.get('nivel_ingles')),
        'user_language_spanish_level': normalize_text(language.get('nivel_espanhol')),
        'user_language_other_level': normalize_text(language.get('outro_idioma')),
        'user_date_of_birth': normalize_text(personal_information.get('data_nascimento')),
        'user_name': normalize_text(personal_information.get('nome')),
        'user_academic_level': normalize_text(language.get('nivel_academico')),
        'user_cv': normalize_text(user_dict.get('cv_pt', '')),
        'user_skills': normalize_text(professional.get('conhecimentos_tecnicos')),
        'user_areas_of_activity': normalize_text(professional.get('area_atuacao')),
        'user_remuneration': normalize_text(professional.get('remuneracao')),
        'user_certifications': normalize_text(professional.get('certificacoes')),
        'user_other_certifications': normalize_text(professional.get('outras_certificacoes')),
        'user_professional_level': normalize_text(professional.get('nivel_profissional')),
        'user_courses': normalize_text(language.get('cursos')),
    }

def extract_job_candidates_info(job_id: int, jobs, users, prospects: List[dict]) -> List :
    job = jobs.get(str(job_id))

    if job is None:
        print(f"Job not found: ID {job_id}.")
        return []

    extract_job = extract_job_info(job_id, job)

    print(f"Job: {job_id} | {extract_job['job_title']}")
    
    rows = []
    for prospect in prospects:
        user_id = prospect.get('codigo')
        user = users.get(str(user_id))

        if user is None:
            print(f"User not found: ID {user_id}.")
            continue

        extract_user = extract_user_info(user_id, user)

        rows.append({
            **extract_user,
            **extract_job,
            'candidate_status': prospect.get('situacao_candidado')
        })

    return rows
