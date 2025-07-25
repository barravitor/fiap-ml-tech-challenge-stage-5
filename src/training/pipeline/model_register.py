import sys
import mlflow
from mlflow.tracking import MlflowClient
from shared.config import SCALE_POS_WEIGHT

EXPETIMENTAL_RUN_ID=''

if not EXPETIMENTAL_RUN_ID:
    print("Erro: EXPETIMENTAL_RUN_ID not found.")
    sys.exit(1)

MODEL_NAME=f"XGBoost_SMOTE_SPW{SCALE_POS_WEIGHT}"

result = mlflow.register_model(
    model_uri=f"runs:/{EXPETIMENTAL_RUN_ID}/model",
    name=MODEL_NAME
)

print(f"Model registered: {result.version}")

client = MlflowClient()
client.set_registered_model_alias(
    name=MODEL_NAME,
    version=result.version,
    alias="Production",
)