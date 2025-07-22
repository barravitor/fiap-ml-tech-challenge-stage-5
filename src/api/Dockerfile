# api/Dockerfile

FROM python:3.10.12-slim

WORKDIR /app

COPY src ./
COPY src/api/start_mlflow.sh ./api/start_mlflow.sh
RUN chmod +x ./api/start_mlflow.sh

COPY requirements.txt ./requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN export PYTHONPATH=$(pwd)/

EXPOSE 8000

CMD ["./api/start_api.sh"]