import re
import pandas as pd
from unidecode import unidecode

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Define stopwords em português
STOP_WORDS = set(stopwords.words('portuguese'))

def normalize_text(text: str) -> str:
    """
    Normaliza o texto:
    - Converte para minúsculas
    - Remove acentuação
    - Remove pontuações
    - Remove stopwords
    - Retorna texto limpo e tokenizado
    """
    if not isinstance(text, str):
        if pd.isna(text):
            return ""
        text = str(text)

    # Normalização inicial
    text = unidecode(text.lower())
    text = re.sub(r"[^\w\s]", " ", text)  # Remove pontuações
    text = re.sub(r"\s+", " ", text).strip()

    # Tokenização e remoção de stopwords
    tokens = word_tokenize(text)
    tokens = [token for token in tokens if token not in STOP_WORDS]
    text = ' '.join(tokens)

    return text

def preprocess_text(text: str):
    text = unidecode(text.lower())
    tokens = re.findall(r'\b\w+\b', text)
    return tokens
