import pandas as pd
from .data_extractors import extract_job_candidates_info

def build_raw_candidate_dataset(jobs, applicants, prospects):
    extend_rows = []
    
    for job_id, prospect in prospects.items():
        if not prospect['prospects']:
            continue

        rows = extract_job_candidates_info(job_id, jobs, applicants, prospect['prospects'])
        extend_rows.extend(rows)

    df = pd.DataFrame(extend_rows)

    return df
