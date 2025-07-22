# api/Dockerfile

FROM python:3.10.12-slim

WORKDIR /app

COPY /requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ /app/api
COPY ./start_api.sh /app/start_api.sh
COPY /src/shared /app/shared

EXPOSE 8000

CMD ["./start_api.sh"]