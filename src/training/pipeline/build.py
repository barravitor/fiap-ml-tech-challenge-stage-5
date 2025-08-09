import pandas as pd

from training.embedding.embed_text import embed_or_missing
from training.preprocessing.dataset import extract_job_candidates_info
from training.preprocessing.geocode import get_geo_distance
from training.features.build_features import process_features
from training.preprocessing.text import concat_text

def candidate_dataset(jobs, applicants, prospects) -> pd.DataFrame:
    extend_rows = []
    
    for job_id, prospect in prospects.items():
        if not prospect['prospects']:
            continue

        rows = extract_job_candidates_info(job_id, jobs, applicants, prospect['prospects'])
        extend_rows.extend(rows)

    return pd.DataFrame(extend_rows)

def candidate_geo_dataset(df_cand: pd.DataFrame, df_geo: pd.DataFrame) -> pd.DataFrame:
    df_cand['job_local'] = df_cand['job_local'].fillna('[missing_location]').str.strip().str.lower()
    df_cand['user_local'] = df_cand['user_local'].fillna('[missing_location]').str.strip().str.lower()

    df_geo_job = df_geo.rename(columns={
        'location': 'job_local',
        'latitude': 'job_latitude',
        'longitude': 'job_longitude'
    })

    df_geo_user = df_geo.rename(columns={
        'location': 'user_local',
        'latitude': 'user_latitude',
        'longitude': 'user_longitude'
    })

    df_merge = df_cand.merge(df_geo_job, how="left", on="job_local")
    df_merge = df_merge.merge(df_geo_user, how="left", on="user_local")

    df_merge['distance_km'] = df_merge.apply(get_geo_distance, axis=1)
    df_merge['distance_km'] = pd.to_numeric(df_merge['distance_km'], errors='coerce').fillna(-1)

    return df_merge

def embed_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.fillna("")

    results = []
    for index, row in df.iterrows():
        print("index:", index)

        row['user_resume_embed'] = embed_or_missing(concat_text(
            row.get('user_professional_title'),
            row.get('user_cv'),
            row.get('user_courses'),
            row.get('user_skills'),
            row.get('user_other_certifications'),
            row.get('user_certifications'),
            row.get('user_areas_of_activity'),
            row.get('user_professional_level'),
        ), "[missing_user_resume]").tolist()

        row['job_resume_embed'] = embed_or_missing(concat_text(
            row.get('job_title'),
            row.get('job_skills'),
            row.get('job_local'),
            row.get('job_areas_of_activity'),
            row.get('job_necessary_behavioral_skills'),
            row.get('job_activities'),
            row.get('job_professional_level'),
        ), "[missing_job_resume]").tolist()

        # Users
        row['user_cv_embed'] = embed_or_missing(row['user_cv'], "[missing_user_cv]").tolist()
        row['user_areas_of_activity_embed'] = embed_or_missing(row['user_areas_of_activity'], "[missing_user_areas_of_activity]").tolist()
        # Jobs
        row['job_areas_of_activity_embed'] = embed_or_missing(row['job_areas_of_activity'], "[missing_job_areas_of_activity]").tolist()

        results.append(row)
    
    df = pd.DataFrame(results)

    cols_to_float = ['user_latitude', 'user_longitude', 'job_latitude', 'job_longitude', 'distance_km']

    for col in cols_to_float:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

def feature_matrix(df: pd.DataFrame) -> pd.DataFrame:
    extracted_features = []

    for index, row in df.iterrows():
        print("index:", index)
        features = process_features(row)
        extracted_features.append(features)

    return extracted_features