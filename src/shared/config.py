# shared/config.py
from dotenv import load_dotenv
import os

load_dotenv(override=True)

PRODUCTION = os.getenv('PRODUCTION', 'false').lower() == 'true'
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
TRAINED_MODEL_FOLDER=os.getenv('TRAINED_MODEL_FOLDER')

if PRODUCTION:
    DEBUG = False

MLFLOW_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI')
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ALGORITHM = os.getenv("ALGORITHM")

STATUS_MAP = {
    # Negative statuses
    'Inscrito': 0,
    'Desistiu': 0,
    'Desistiu da Contratação': 0,
    'Não Aprovado pelo Cliente': 0,
    'Não Aprovado pelo RH': 0,
    'Não Aprovado pelo Requisitante': 0,
    'Recusado': 0,
    'Sem interesse nesta vaga': 0,
    # Intermediate statuses
    'Em avaliação pelo RH': 0,
    'Encaminhado ao Requisitante': 1,
    'Entrevista Técnica': 1,
    'Entrevista com Cliente': 1,
    'Encaminhar Proposta': 1,
    'Documentação CLT': 1,
    'Documentação Cooperado': 1,
    'Documentação PJ': 1,
    # Success status
    'Aprovado': 1,
    'Contratado como Hunting': 1,
    'Contratado pela Decision': 1,
    'Proposta Aceita': 1,
}

# 
RANDOM_STATE=42
TEST_SIZE_SPLIT=0.2
THRESHOLD=0.42
SCALE_POS_WEIGHT=2
N_ESTIMATORS=100
MAX_DEPTH=8
LEARNING_RATE=0.1
EVAL_METRIC='logloss'
SUBSAMPLE=0.7
COLSAMPLE_BYTREE=1
MIN_CHILD_WEIGHT=1
N_THREAD=1