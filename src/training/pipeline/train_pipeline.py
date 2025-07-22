import os
import pandas as pd
from training.data.data_loader import load_json_file
from training.data.build_dataset import build_raw_candidate_dataset
from training.pipeline.feature_engineering import process_features
from training.pipeline.feature_storage import save_features, load_features

from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import train_test_split
from training.pipeline.model_training import train_model
from training.pipeline.model_evaluation import evaluate_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JOBS = load_json_file(f"{os.path.join(BASE_DIR, '..', '..', '..', 'data')}/jobs.json")
APPLICANTS = load_json_file(f"{os.path.join(BASE_DIR, '..', '..', '..', 'data')}/applicants.json")
PROSPECTS = load_json_file(f"{os.path.join(BASE_DIR, '..', '..', '..', 'data')}/prospects.json")

SKILLS_KEYWORDS = load_json_file(f"{os.path.join(BASE_DIR, '..', '..', 'shared', 'keywords')}/skill_keywords.json")
PROFESSIONALS_KEYWORDS = load_json_file(f"{os.path.join(BASE_DIR, '..', '..', 'shared', 'keywords')}/professional_exp_keywords.json")

# # df = build_raw_candidate_dataset(JOBS, APPLICANTS, PROSPECTS)

df = pd.read_csv(f"{os.path.join(BASE_DIR, '..', 'data', 'raw')}/extract_job_candidates.csv")
print(df.head())

extracted_features = []
y = []
for index, row in df.iterrows():
    print("index:", index)
    features = process_features(row)
    extracted_features.append(features)
    y.append(row["candidate_status"])

# Criar um DataFrame
df_features = pd.DataFrame(extracted_features)
df_features.fillna(0, inplace=True)
print(df_features.shape)

feature_names = df_features.columns.tolist()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_features)

save_features(X_scaled, y, path=f"{os.path.join(BASE_DIR, '..', 'data', 'processed')}/features_dataset.npz")

X_scaled, y = load_features(path=f"{os.path.join(BASE_DIR, '..', 'data', 'processed')}/features_dataset.npz")

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

ros = RandomOverSampler(random_state=42)
X_train_resampled, y_train_resampled = ros.fit_resample(X_train, y_train)

print("Antes do balanceamento:", sum(y_train))
print("Depois do balanceamento:", sum(y_train_resampled))

model = train_model(X_train_resampled, y_train_resampled)
evaluate_model(model, X_test, y_test)








def lol():
    import numpy as np
    import matplotlib.pyplot as plt

    importances = model.feature_importances_
    feat_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    }).sort_values(by='importance', ascending=False)

    # Mostra as 20 mais importantes
    print(feat_df.head(20))

    # Ordena pela importância
    indices = np.argsort(importances)[::-1]

    # Exibe os 20 principais
    # plt.figure(figsize=(12, 6))
    # plt.title("Top 20 Features Mais Importantes")
    # plt.bar(range(20), importances[indices[:20]], align="center")
    # plt.xlabel("Índice da Feature")
    # plt.ylabel("Importância")
    # plt.xticks(range(20), indices[:20])
    # plt.savefig(f'./scatter_real_vs_pred.png')
    # plt.close()

    plt.figure(figsize=(10, 6))
    plt.barh(feat_df['feature'][:20][::-1], feat_df['importance'][:20][::-1])
    plt.title("Top 20 Features Mais Importantes")
    plt.xlabel("Importância")
    plt.tight_layout()
    plt.savefig(f'./scatter_real_vs_pred.png')
    plt.close()

lol()