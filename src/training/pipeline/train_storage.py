import os
import joblib
import mlflow
import numpy as np
from xgboost import XGBClassifier

def save_features(X, y, path='data/processed/features_dataset.npz'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    np.savez(path, X=X, y=y)

def load_features(path='data/processed/features_dataset.npz'):
    data = np.load(path)
    return data['X'], data['y']

def save_scaler(scaler, path='data/processed/scaler.pkl'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(scaler, path)

def load_scaler(path='data/processed/scaler.pkl'):
    return joblib.load(path)

def save_model(model, path='data/processed/model.pkl'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)

def load_model(path='data/processed/model.pkl'):
    return joblib.load(path)

def load_mlflow_model(model_name: str, version: int = None) -> XGBClassifier:
    mlflow_model_uri = f"models:/{model_name}/{version}"
    mlflow_model: XGBClassifier = mlflow.xgboost.load_model(mlflow_model_uri)
    return mlflow_model

def get_or_load_model(model_name: str, version: int = None) -> XGBClassifier:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    cache_path = f"{os.path.join(BASE_DIR, '..', 'data', 'processed')}/{model_name}_version_{version}_cached.pkl"

    if os.path.exists(cache_path):
        return load_model(cache_path)
    
    model = load_mlflow_model(model_name, version)
    save_model(model, cache_path)

    return model
