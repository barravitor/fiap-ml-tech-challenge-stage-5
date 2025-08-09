import json
import os
from matplotlib import pyplot as plt
import mlflow
import numpy as np
import pandas as pd
import xgboost as xgb
from imblearn.over_sampling import SMOTE
from sklearn.metrics import (
    f1_score, recall_score, roc_curve, auc, precision_recall_curve,
    average_precision_score, classification_report, ConfusionMatrixDisplay,
    accuracy_score
)
from sklearn.model_selection import train_test_split
from training.pipeline.model_register import register_model
from training.preprocessing.geocode import generate_geocodes
from training.preprocessing.data_loader import load_json_file
from training.pipeline.build import candidate_dataset, candidate_geo_dataset, embed_dataset, feature_matrix
from training.pipeline.train_storage import save_features, save_model
from training.model.xgboost import train
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

VERSION=1

DATA_INTERIM_CAND = f"data/interim/candidates_{VERSION}.csv"
DATA_INTERIM_GEO = f"data/interim/geocodes_{VERSION}.csv"
DATA_INTERIM_CAND_PLUS_GEO = f"data/interim/candidates_geo_{VERSION}.csv"
DATA_INTERIM_EMBED = f"data/interim/embeddings_{VERSION}.parquet"
MODEL_OUTPUT = f"outputs/models/model_{VERSION}.pkl"
FEATURES_OUTPUT = f"outputs/features/features_dataset_{VERSION}.npz"
PREDICTIONS_OUTPUT = f"outputs/predictions/preds_{VERSION}.csv"

def main():
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

            print("-------------------------------------------------------------------------------------------------------------------------------")
            print("Etapa 1: Lendo dados brutos...")
            JOBS = load_json_file("./data/raw/vagas.json")
            APPLICANTS = load_json_file("./data/raw/applicants.json")
            PROSPECTS = load_json_file("./data/raw/prospects.json")

            df_raw: pd.DataFrame
            if not os.path.isfile(DATA_INTERIM_CAND):
                print("Arquivo não encontrado, executando o bloco if")
                df_raw = candidate_dataset(JOBS, APPLICANTS, PROSPECTS)
                os.makedirs(os.path.dirname(DATA_INTERIM_CAND), exist_ok=True)
                df_raw.to_csv(DATA_INTERIM_CAND, index=False, encoding="utf-8")
            else:
                print("Arquivo encontrado, executando o load do arquivo")
                df_raw = pd.read_csv(DATA_INTERIM_CAND)

            print("-------------------------------------------------------------------------------------------------------------------------------")
            print("Etapa 2: Gerando geocodificação...")
            df_geo: pd.DataFrame
            if not os.path.isfile(DATA_INTERIM_GEO):
                print("Arquivo não encontrado, executando o bloco if")
                df_geo = generate_geocodes(df_raw)
                os.makedirs(os.path.dirname(DATA_INTERIM_GEO), exist_ok=True)
                df_geo.to_csv(DATA_INTERIM_GEO, index=False, encoding="utf-8")
            else:
                print("Arquivo encontrado, executando o load do arquivo")
                df_geo = pd.read_csv(DATA_INTERIM_GEO)

            print("-------------------------------------------------------------------------------------------------------------------------------")
            print("Etapa 3: Adicionando location...")
            df_cand_geo: pd.DataFrame
            if not os.path.isfile(DATA_INTERIM_CAND_PLUS_GEO):
                print("Arquivo não encontrado, executando o bloco if")
                df_cand_geo = candidate_geo_dataset(df_raw, df_geo)
                os.makedirs(os.path.dirname(DATA_INTERIM_CAND_PLUS_GEO), exist_ok=True)
                df_cand_geo.to_csv(DATA_INTERIM_CAND_PLUS_GEO, index=False, encoding="utf-8")
            else:
                print("Arquivo encontrado, executando o load do arquivo")
                df_cand_geo = pd.read_csv(DATA_INTERIM_CAND_PLUS_GEO)

            print("-------------------------------------------------------------------------------------------------------------------------------")
            print("Etapa 4: Gerando embeddings...")
            df_embed: pd.DataFrame
            if not os.path.isfile(DATA_INTERIM_EMBED):
                print("Arquivo não encontrado, executando o bloco if")
                df_embed = embed_dataset(df_cand_geo)
                os.makedirs(os.path.dirname(DATA_INTERIM_EMBED), exist_ok=True)
                df_embed.to_parquet(DATA_INTERIM_EMBED, index=False)
            else:
                print("Arquivo encontrado, executando o load do arquivo")
                df_embed = pd.read_parquet(DATA_INTERIM_EMBED)

            print("-------------------------------------------------------------------------------------------------------------------------------")
            print("Etapa 5: Construindo matriz de features...")
            extracted_features = feature_matrix(df_embed)

            features = [{k: v for k, v in feature.items() if k != 'target'} for feature in extracted_features]
            targets = [{k: v for k, v in feature.items() if k == 'target'} for feature in extracted_features]
            features_name = list(features[0].keys())

            X = np.array([np.concatenate(list(feature.values())) for feature in features], dtype=np.float32)
            y = np.array([target['target'] for target in targets], dtype=np.float32)

            print("-------------------------------------------------------------------------------------------------------------------------------")
            print("Etapa 6: Treinando modelo...")
            print(X.shape)
            save_features(X, y, FEATURES_OUTPUT)

            mlflow.log_param("total_samples", len(X))
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE_SPLIT, random_state=RANDOM_STATE, stratify=y)

            mlflow.log_param("train_class_total", str(np.bincount(y_train.astype(int)).tolist()))
            mlflow.log_param("test_class_total", str(np.bincount(y_test.astype(int)).tolist()))

            smote = SMOTE(random_state=RANDOM_STATE)
            X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

            model = train(X_train_res, y_train_res, X_test, y_test)

            save_model(model, MODEL_OUTPUT)

            mlflow.xgboost.log_model(
                xgb_model=model,
                name="model",
                registered_model_name="XGB_SMOTE",
                pip_requirements="requirements.txt",
                input_example=X_test[:2],
                signature=None,
            )

            print("-------------------------------------------------------------------------------------------------------------------------------")
            print("Etapa 7: Rodando predições...")

            results = model.evals_result()

            # === 1. Gerar previsões ===
            y_true = y_test
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            y_pred_threshold = (y_pred_proba >= THRESHOLD).astype(int)

            # === 2. Métricas baseadas em probabilidade ===
            precision, recall, thresholds = precision_recall_curve(y_true, y_pred_proba)
            average_precision = average_precision_score(y_true, y_pred_proba)
            fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
            roc_auc = auc(fpr, tpr)

            # === 3. Métricas baseadas em classe (threshold aplicado) ===
            accuracy = accuracy_score(y_true, y_pred_threshold)
            f1_class1 = f1_score(y_true, y_pred_threshold, pos_label=1)
            recall_class1 = recall_score(y_true, y_pred_threshold, pos_label=1)

            # Logar no MLflow
            mlflow.log_metric("average_precision", average_precision)
            mlflow.log_metric("roc_auc", roc_auc)
            mlflow.log_metric("f1_class1", f1_class1)
            mlflow.log_metric("recall_class1", recall_class1)
            mlflow.log_metric("accuracy", accuracy)

            # === 5. Prints no console ===
            print("Acurácia:", accuracy)
            print("F1 Score (classe 1):", f1_class1)
            print("Recall (classe 1):", recall_class1)
            print("Average Precision (PR AUC):", average_precision)
            print("AUC ROC:", roc_auc)
            print("Relatório de Classificação:\n", classification_report(y_true, y_pred_threshold))

            # -------------------------------------------------------------------------------------------------- #
            # IMAGE GRAFIC: ROC Curve
            plt.figure(figsize=(10, 6))
            plt.plot(fpr, tpr, label=f'AUC = {roc_auc:.2f}')
            plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title('ROC Curve')
            plt.legend()
            mlflow.log_figure(plt.gcf(), "roc_curve.png")
            plt.close()

            # -------------------------------------------------------------------------------------------------- #
            # IMAGE GRAFIC: Precision-Recall Curve
            plt.figure(figsize=(10, 6))
            plt.plot(recall, precision, label=f'AP = {average_precision:.2f}')
            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.title('Precision-Recall Curve')
            plt.legend()
            mlflow.log_figure(plt.gcf(), "precision_recall_curve.png")
            plt.close()

            # # -------------------------------------------------------------------------------------------------- #
            # # IMAGE GRAFIC: XGBoost Feature Importance
            # fig, ax = plt.subplots(figsize=(16, 6))  # Tamanho personalizado
            # xgb.plot_importance(model, max_num_features=20, ax=ax)
            # yticklabels = [
            #     features_name[int(f[1:])] if int(f[1:]) < len(features_name) else f
            #     for f in model.get_booster().get_fscore().keys()
            # ]
            # ax.set_yticklabels(yticklabels)
            # plt.title('XGBoost Feature Importance')
            # mlflow.log_figure(plt.gcf(), "feature_importance.png")
            # plt.close()

            # -------------------------------------------------------------------------------------------------- #
            # IMAGE GRAFIC: Learning Curve
            plt.figure(figsize=(16, 6))
            plt.plot(results['validation_0']['logloss'], label='Train')
            plt.plot(results['validation_1']['logloss'], label='Validation')
            plt.xlabel('Rounds')
            plt.ylabel('Log Loss')
            plt.title('Learning Curve')
            plt.legend()
            mlflow.log_figure(plt.gcf(), "learning_curve.png")
            plt.close()

            # -------------------------------------------------------------------------------------------------- #
            # IMAGE GRAFIC: Confusion Matrix
            fig, ax = plt.subplots(figsize=(10, 6))
            disp = ConfusionMatrixDisplay.from_predictions(
                y_true,
                y_pred_threshold,
                display_labels=["Não contratado", "Contratado"],
                cmap="viridis",
                values_format='d',
                ax=ax
            )
            ax.set_title("Confusion Matrix")
            mlflow.log_figure(fig, "confusion_matrix.png")
            plt.close(fig)

            # -------------------------------------------------------------------------------------------------- #
            # IMAGE GRAFIC: Precision vs Recall x Threshold
            plt.figure(figsize=(10, 6))
            plt.plot(thresholds, precision[:-1], label='Precision')
            plt.plot(thresholds, recall[:-1], label='Recall')
            plt.xlabel('Threshold')
            plt.ylabel('Score')
            plt.title('Precision vs Recall x Threshold')
            plt.legend()
            plt.grid(True)
            mlflow.log_figure(plt.gcf(), "precision_vs_recall_x_threshold.png")
            plt.close()

            register_model(run_id)

if __name__ == "__main__":
    main()
