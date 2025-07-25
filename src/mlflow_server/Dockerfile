# mlflow_server/Dockerfile

FROM python:3.10.12-slim

USER root

# Installing system dependencies
RUN apt-get update && apt-get install -y nginx apache2-utils supervisor wget

RUN rm -rf /var/lib/apt/lists/*

# Copy the code and configuration files
WORKDIR /app

COPY src/mlflow_server ./
COPY src/mlflow_server/start_mlflow.sh ./start_mlflow.sh
RUN chmod +x ./start_mlflow.sh

COPY requirements.txt ./requirements.txt

# Install mlflow and other Python libs
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the nginx password and config file to where nginx expects it
COPY src/mlflow_server/.htpasswd /etc/nginx/.htpasswd
COPY src/mlflow_server/nginx.conf /etc/nginx/sites-enabled/default

# Copy the supervisord.conf file to the expected location
COPY src/mlflow_server/supervisord.conf /etc/supervisor/supervisord.conf

# Expose port 80 (nginx)
EXPOSE 80

# Run supervisor to manage nginx + mlflow
CMD ["supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]

# EXPOSE 5000
# CMD ["./start_mlflow.sh"]

