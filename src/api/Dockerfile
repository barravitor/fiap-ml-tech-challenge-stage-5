# api/Dockerfile

FROM python:3.10.12-slim

WORKDIR /app

COPY ./ ./
COPY src/api/start_api.sh ./src/api/start_api.sh
RUN chmod +x ./src/api/start_api.sh

COPY requirements.txt ./requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN export PYTHONPATH=$(pwd)/src

EXPOSE 8000

CMD ["./src/api/start_api.sh"]