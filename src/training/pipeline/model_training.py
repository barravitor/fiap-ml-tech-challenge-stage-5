from xgboost import XGBClassifier
from shared.config import (
    RANDOM_STATE,
    SCALE_POS_WEIGHT,
    EVAL_METRIC,
    MAX_DEPTH,
    N_ESTIMATORS,
    LEARNING_RATE,
    SUBSAMPLE,
    COLSAMPLE_BYTREE,
    MIN_CHILD_WEIGHT,
)

def train_model(X_train, y_train):
    model = XGBClassifier(
        scale_pos_weight=SCALE_POS_WEIGHT,
        eval_metric=EVAL_METRIC,
        random_state=RANDOM_STATE,
        n_estimators=N_ESTIMATORS,
        max_depth=MAX_DEPTH,
        learning_rate=LEARNING_RATE,
        subsample=SUBSAMPLE,
        colsample_bytree=COLSAMPLE_BYTREE,
        min_child_weight=MIN_CHILD_WEIGHT
    )

    model.fit(X_train, y_train)
    return model