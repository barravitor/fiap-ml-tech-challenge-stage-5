# FIAP TECH CHALLENGE | Datathon 

## Index

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation and Run](#installation-and-run)
- [Contribution](#contribution)
- [License](#license)
- [Contact](#contact)

## Introduction

This project was developed for the **FIAP Tech Challenge – Datathon**, where the main goal is to create a machine learning solution that evaluates the compatibility (**fit**) between a job opportunity and a candidate profile.

Our solution includes:
- A REST API built with FastAPI that receives job and user data and returns a binary prediction (fit or not fit), along with the confidence probability.
- A machine learning pipeline for training, validating, and managing models using **MLflow**.
- A modular architecture to allow scalability and integration with real-world HR platforms.

## 🚀 Features

- ✅ Machine learning model to predict candidate-job compatibility
- 🔌 RESTful API using FastAPI
- 📊 Model management and versioning with MLflow
- 🧪 Modular preprocessing and feature engineering
- 🔐 Token-based security layer (for future integration)
- 📝 Automatically generated API docs at `/docs`
- 🐍 Compatible with Python 3.10

- **🧪 RESTful API with FastAPI**  
  Interface for integration with external systems.

  **Available Endpoints:**
  - `POST /api/public/predict`: Sends input data and receives forecast output
  - `GET /`: Checks API health status

- [API Swagger](https://fiap-ml-tech-challenge-stage-5-production.up.railway.app/docs)

## Technologies Used

- [Python 3.10](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [MLflow](https://mlflow.org/)
- [scikit-learn](https://scikit-learn.org/)
- [pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [httpx](https://www.python-httpx.org/) – for external requests
- [New Relic (optional)](https://newrelic.com/) – for performance monitoring

## Installation and run

Instructions on how to install and run the project locally.

---

### ✅ 1. Environment Setup
Create a .env file in the project root following the example in the .env-example file

Required python version: 3.10.12

```bash
python3.10 -m venv .venv   # Run to create the environment
source venv/bin/activate   # On Linux/macOS
venv\Scripts\activate.bat  # On Windows
export PYTHONPATH=$(pwd)/src
pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt # Run to install the necessary packages
python -m nltk.downloader all
```

---

### 📊 2. MLflow
Run the mlflow
```bash
./start_mlflow.sh
```

Once executed, open your browser and access:

👉 http://localhost:5000

This will open the MLflow dashboard, where you can track experiments, models, and metrics.

---

### 🧠 3. Model Training

Before running the training pipeline, make sure to create a folder named `data` in the root of the project and place inside it the 3 JSON files provided by **Decision**.

**Expected folder structure:**

```
/data
 ├─ applicants.json
 ├─ prospects.json
 └─ vagas.json
```

To start the training process, run:

```bash
python ./src/training/pipeline/train_pipeline.py
```

This will execute the full training pipeline using the provided data.

---

## 🌐 4. API

Start the REST API with the following command:

```bash
./start_api.sh
```

Once running, the API will be available at:

👉 http://localhost:8000

You can now send requests to the API to interact with the trained model.

---

## Contribution

We welcome contributions to this project! Here’s how you can help:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Make your changes and commit them (`git commit -m 'feat: Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a Pull Request.

Please ensure that your code adheres to the project's coding standards and includes appropriate tests where necessary.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.

## Contact

For questions, suggestions, or feedback, please contact:

* **Edson Vitor**  
  GitHub: [barravitor](https://github.com/barravitor)