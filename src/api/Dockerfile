# api/Dockerfile

FROM python:3.10.12-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./

RUN export PYTHONPATH=$(pwd)/

EXPOSE 8000

CMD ["./api/start_api.sh"]