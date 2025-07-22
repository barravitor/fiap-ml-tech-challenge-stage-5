import joblib
import numpy as np

def save_features(X, y, path='data/processed/features_dataset.npz'):
    np.savez(path, X=X, y=y)

def load_features(path='data/processed/features_dataset.npz'):
    data = np.load(path)
    return data['X'], data['y']

def save_scaler(scaler, path='data/processed/scaler.pkl'):
    joblib.dump(scaler, path)

def load_scaler(path='data/processed/scaler.pkl'):
    return joblib.load(path)

def save_model(model, path='data/processed/model.pkl'):
    joblib.dump(model, path)

def load_model(path='data/processed/model.pkl'):
    return joblib.load(path)
