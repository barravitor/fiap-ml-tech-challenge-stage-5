set -a
source .env
set +a

mkdir -p $MLFLOW_ARTIFACT_PATH

mlflow server \
  --backend-store-uri $MLFLOW_DB_PATH \
  --default-artifact-root $MLFLOW_ARTIFACT_PATH \
  --host 0.0.0.0 \
  --port 5000