#!/bin/bash

echo "$GOOGLE_CREDENTIALS_JSON" > ./gcp-storage-service-account.json

ls -l "$GOOGLE_APPLICATION_CREDENTIALS"

python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')"

newrelic-admin run-program uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 1