# api/Dockerfile

FROM python:3.10.12-slim

WORKDIR /app

COPY src ./
COPY src/api/start_api.sh ./api/start_api.sh
RUN chmod +x ./api/start_api.sh

COPY requirements.txt ./requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')"

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["api/start_api.sh"]