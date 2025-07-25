import sys
import mlflow
from mlflow.tracking import MlflowClient
from shared.config import SCALE_POS_WEIGHT

def register_model(run_id: str):
    if not run_id:
        print("Erro: run_id not found.")
        sys.exit(1)

    MODEL_NAME=f"XGBoost_SMOTE_SPW{SCALE_POS_WEIGHT}"

    result = mlflow.register_model(
        model_uri=f"runs:/{run_id}/model",
        name=MODEL_NAME
    )

    print(f"Model registered: {result.version}")

    client = MlflowClient()
    client.set_registered_model_alias(
        name=MODEL_NAME,
        version=result.version,
        alias="Production",
    )
