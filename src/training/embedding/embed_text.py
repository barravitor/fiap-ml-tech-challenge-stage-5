import torch
import numpy as np
from tqdm import tqdm

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2', device="cuda" if torch.cuda.is_available() else "cpu")

def embed_or_missing(text: str, tag="[missing]"):
    return model.encode(text if text.strip() else tag, batch_size=256, show_progress_bar=True, device="cuda" if torch.cuda.is_available() else "cpu")

def missing_flag(text: str):
    return int(not text.strip())

def cosine_sim(a, b):
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    return np.dot(a, b) / (na * nb) if na > 0 and nb > 0 else 0.0

def embed_column(df, col, tag):
    tqdm.pandas(desc=f"Embedding {col}")
    embed_col = f"{col}_embed"
    df[embed_col] = df[col].progress_apply(lambda x: embed_or_missing(x, tag).tolist())
    return embed_col, df[embed_col]