# /training/data/exploratory_data_analysis.py

import os
from data_loader import load_json_file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JOBS = load_json_file(f"{os.path.join(BASE_DIR, '..', '..', '..', 'data')}/vagas.json")
APPLICANTS = load_json_file(f"{os.path.join(BASE_DIR, '..', '..', '..', 'data')}/applicants.json")
PROSPECTS = load_json_file(f"{os.path.join(BASE_DIR, '..', '..', '..', 'data')}/prospects.json")

# Analisar os status dos candidatos
status_set = set()

for job_id, document in PROSPECTS.items():
    for prospect in document.get("prospects", []):
        status = prospect.get("situacao_candidado", "").strip()
        if status:
            status_set.add(status)

print("Situações únicas dos candidatos:")
for s in sorted(status_set):
    print("-", s)
