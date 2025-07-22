import numpy as np

def save_features(X, y, path='data/processed/features_dataset.npz'):
    np.savez(path, X=X, y=y)

def load_features(path='data/processed/features_dataset.npz'):
    data = np.load(path)
    return data['X'], data['y']
