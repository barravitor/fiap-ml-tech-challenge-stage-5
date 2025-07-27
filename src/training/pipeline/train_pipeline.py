import json
import os
import time
import mlflow
import numpy as np
import pandas as pd
from training.data.data_loader import load_json_file
from training.data.build_dataset import build_raw_candidate_dataset
from training.pipeline.feature_engineering import process_features
from training.pipeline.train_storage import load_features, save_features, save_model
from training.pipeline.model_training import train_model
from training.pipeline.model_evaluation import evaluate_model
from training.pipeline.model_register import register_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, precision_recall_curve
from imblearn.over_sampling import SMOTE
from sklearn.metrics import f1_score, recall_score
from shared.config import (
    MLFLOW_TRACKING_URI,
    RANDOM_STATE,
    TEST_SIZE_SPLIT,
    THRESHOLD,
    SCALE_POS_WEIGHT,
    EVAL_METRIC,
    MAX_DEPTH,
    N_ESTIMATORS,
    LEARNING_RATE,
    SUBSAMPLE,
    COLSAMPLE_BYTREE,
    MIN_CHILD_WEIGHT,
    STATUS_MAP,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JOBS = load_json_file(f"{os.path.join(BASE_DIR, '..', '..', '..', 'data')}/vagas.json")
APPLICANTS = load_json_file(f"{os.path.join(BASE_DIR, '..', '..', '..', 'data')}/applicants.json")
PROSPECTS = load_json_file(f"{os.path.join(BASE_DIR, '..', '..', '..', 'data')}/prospects.json")
FILE_PATH = f"{os.path.join(BASE_DIR, '..', 'data', 'raw')}/extract_job_candidates.csv"

df: pd.DataFrame

if not os.path.isfile(FILE_PATH):
    print("Arquivo não encontrado, executando o bloco if")
    df = build_raw_candidate_dataset(JOBS, APPLICANTS, PROSPECTS)
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    df.to_csv(FILE_PATH, index=False, encoding="utf-8")
else:
    print("Arquivo encontrado, executando o load do arquivo")
    df = pd.read_csv(FILE_PATH)

df = df.fillna("")
print(df.head())

if __name__ == "__main__":
    start_time = time.time()
    mlflow.set_experiment("FIAP ML STAGE 5 | DATATHON")
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    with mlflow.start_run(run_name=f"XGBoost_SMOTE_SPW{SCALE_POS_WEIGHT}", description="Tech Challenge 5") as run:
        if mlflow.active_run():
            run_id = run.info.run_id
            print("Run ID:", run_id)

            mlflow.set_tag("model_type", "XGBoost")
            mlflow.set_tag("balance_strategy", "SMOTE")
            mlflow.set_tag("threshold_strategy", f"Custom threshold {THRESHOLD}")
            mlflow.set_tag("run_description", "XGBoost model to predict the fit between candidates and vacancies, focusing on class 1 recall (candidates with a good profile)")
            mlflow.set_tag("target_metric", "recall_class_1")
            mlflow.set_tag("STATUS_MAP", json.dumps(STATUS_MAP, ensure_ascii=False))

            mlflow.log_param("scale_pos_weight", SCALE_POS_WEIGHT)
            mlflow.log_param("threshold", THRESHOLD)
            mlflow.log_param("sampling_ratio", "1:1")
            mlflow.log_param("random_state", RANDOM_STATE)
            mlflow.log_param("test_size", TEST_SIZE_SPLIT)
            mlflow.log_param("eval_metric", EVAL_METRIC)
            mlflow.log_param("subsample", SUBSAMPLE)
            mlflow.log_param("colsample_bytree", COLSAMPLE_BYTREE)
            mlflow.log_param("min_child_weight", MIN_CHILD_WEIGHT)
            mlflow.log_param("max_depth", MAX_DEPTH)
            mlflow.log_param("learning_rate", LEARNING_RATE)
            mlflow.log_param("n_estimators", N_ESTIMATORS)

            extracted_features = []
            y = []
            for index, row in df.iterrows():
                print("index:", index)
                features, target = process_features(row)
                extracted_features.append(features)
                y.append(target)

            X = np.array(extracted_features)
            y = np.array(y)

            save_features(X, y, f"{os.path.join(BASE_DIR, '..', 'data', 'processed')}/features_dataset.npz")

            mlflow.log_param("total_samples", len(X))
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE_SPLIT, random_state=RANDOM_STATE, stratify=y)

            mlflow.log_param("train_class_total", str(np.bincount(y_train).tolist()))
            mlflow.log_param("test_class_total", str(np.bincount(y_test).tolist()))

            smote = SMOTE(random_state=RANDOM_STATE)
            X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

            model = train_model(X_train_res, y_train_res)
            evaluate_model(model, X_test, y_test)

            save_model(model, path=f"{os.path.join(BASE_DIR, '..', 'data', 'processed')}/model.pkl")

            mlflow.xgboost.log_model(
                xgb_model=model,
                name="model",
                registered_model_name="XGB_SMOTE",
                pip_requirements="requirements.txt",
                input_example=X_test[:2],
                signature=None,
            )

            probas = model.predict_proba(X_test)[:, 1]
            y_pred = (probas >= THRESHOLD).astype(int)

            f1_class1 = f1_score(y_test, y_pred, pos_label=1)
            recall_class1 = recall_score(y_test, y_pred, pos_label=1)

            mlflow.log_metric("f1_class1", f1_class1)
            mlflow.log_metric("recall_class1", recall_class1)

            end_time = time.time()
            training_duration = end_time - start_time
            mlflow.log_metric("training_time_in_seconds", training_duration)

            register_model(run_id)
















































































            # X, y = load_features(f"{os.path.join(BASE_DIR, '..', 'data', 'processed')}/features_dataset.npz")

            # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE_SPLIT, random_state=RANDOM_STATE, stratify=y)

            # smote = SMOTE(random_state=RANDOM_STATE)
            # X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

            # model = train_model(X_train, y_train)
            # evaluate_model(model, X_test, y_test)

            # save_model(model, path=f"{os.path.join(BASE_DIR, '..', 'data', 'processed')}/model.pkl")












            # model = load_model(path=f"{os.path.join(BASE_DIR, '..', 'data', 'processed')}/model.pkl")

            # X, y = load_features(f"{os.path.join(BASE_DIR, '..', 'data', 'processed')}/features_dataset.npz")

            # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE_SPLIT, random_state=RANDOM_STATE, stratify=y)

            # # Gerar probabilidades
            # y_proba = model.predict_proba(X_test)[:, 1]  # probabilidade da classe 1

            # # Ajustar threshold (ex: 0.4)
            # y_pred_threshold = (y_proba >= THRESHOLD).astype(int)

            # # Avaliar
            # print("Threshold:", THRESHOLD)
            # print(classification_report(y_test, y_pred_threshold))




















            # def lol1():
            #     import matplotlib.pyplot as plt

            #     precision, recall, thresholds = precision_recall_curve(y_test, probas)
            #     print(precision)
            #     print(recall)
            #     print(thresholds)

            #     plt.figure(figsize=(10, 6))
            #     plt.plot(thresholds, precision[:-1], label='Precision')
            #     plt.plot(thresholds, recall[:-1], label='Recall')
            #     plt.xlabel('Threshold')
            #     plt.ylabel('Score')
            #     plt.title('Precision vs Recall x Threshold')
            #     plt.legend()
            #     plt.grid(True)
            #     plt.savefig(f'./scatter_real_vs_pred.png')
            #     plt.close()

            # lol1()
