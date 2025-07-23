# shared/config.py
from dotenv import load_dotenv
import os

load_dotenv(override=True)

PRODUCTION = os.getenv('PRODUCTION', 'false').lower() == 'true'
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

if PRODUCTION:
    DEBUG = False

MLFLOW_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI')
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ALGORITHM = os.getenv("ALGORITHM")

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