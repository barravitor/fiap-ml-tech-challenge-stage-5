#!/bin/bash

echo "$GOOGLE_CREDENTIALS_JSON" > ./gcp-storage-service-account.json

ls -l "$GOOGLE_APPLICATION_CREDENTIALS"

export PYTHONPATH=$(pwd)/src

newrelic-admin run-program uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 1