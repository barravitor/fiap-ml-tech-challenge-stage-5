# api/Dockerfile

FROM python:3.10.12-slim

WORKDIR /app

COPY /requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY /src/api /app/src/api
COPY /src/api/start_api.sh /app/src/api/start_api.sh
COPY /src/shared /app/src/shared

RUN export PYTHONPATH=$(pwd)/src

EXPOSE 8000

CMD ["/app/src/api/start_api.sh"]