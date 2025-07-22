from sklearn.ensemble import RandomForestClassifier
import lightgbm as lgb

n_estimators=200
max_depth=8
random_state=42

# def train_model(X_train, y_train):
#     model = lgb.LGBMClassifier(
#         n_estimators=n_estimators,
#         max_depth=max_depth,
#         class_weight='balanced',
#         random_state=random_state
#     )
#     model.fit(X_train, y_train)
#     return model

def train_model(X_train, y_train):
    model = RandomForestClassifier(class_weight='balanced', n_estimators=n_estimators, max_depth=max_depth, random_state=random_state)
    model.fit(X_train, y_train)
    return model