import os
import pandas as pd
from .data_extractors import extract_job_candidates_info

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILES_PATH = os.path.join(BASE_DIR, 'raw')

def build_raw_candidate_dataset(jobs, applicants, prospects):
    extend_rows = []
    
    for job_id, prospect in prospects.items():
        if not prospect['prospects']:
            continue

        rows = extract_job_candidates_info(job_id, jobs, applicants, prospect['prospects'])
        extend_rows.extend(rows)

    df = pd.DataFrame(extend_rows)
    df.to_csv(f"{DATA_FILES_PATH}/extract_job_candidates.csv", index=False, encoding="utf-8")

    return df
