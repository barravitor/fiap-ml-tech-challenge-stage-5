# Load .env
set -a
source .env
set +a

export PYTHONPATH=$(pwd)/src

python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')"

newrelic-admin run-program uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir src/api --reload-dir src/shared