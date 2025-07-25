# api/routes/public_routes.py
import os
import httpx
import numpy as np
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from mlflow.tracking import MlflowClient
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from api.schemas.index_schemas import LoginSchema, TokenSchema, UserRoleSchema
from shared.db.models.index_models import RecruiterModelDb, CompanyModelDb, UserModelDb
from shared.db.database import get_session_local
from datetime import datetime, timezone
from shared.utils.jwt_helper import create_jwt_token
from training.data.build_dataset import build_raw_candidate_dataset
from training.pipeline.feature_engineering import process_features
from training.pipeline.train_storage import get_or_load_model
from shared.config import THRESHOLD, SCALE_POS_WEIGHT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

public_router = APIRouter()
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# @public_router.post("/auth/login", response_model=TokenSchema,
#     responses={
#         200: {
#             "description": "Returns an access token.",
#             "content": {
#                 "application/json": {
#                     "schema": TokenSchema.model_json_schema(),
#                     "example": {
#                         "access_token": "token_jwt_generated",
#                         "token_type": "bearer"
#                     }
#                 }
#             }
#         },
#         400: {
#             "description": "Bad Request.",
#             "content": {
#                 "application/json": {
#                     "examples": {
#                         "incorrect_email_or_password": {
#                             "summary": "Incorrect email or password",
#                             "value": {
#                                 "detail": "Incorrect email or password"
#                             }
#                         }
#                     }
#                 }
#             }
#         }
#     }
# )
# def login(login: LoginSchema, db: Session = Depends(get_session_local)):
#     """
#     Login the recruiter into the platform.
    
#     - **Return**: An access token on success.

#     ## Possible Errors:
#     - **400 Bad Request**: If are incorrect email or password.
#     """

#     access_token: str

#     if login.role == UserRoleSchema.recruiter:
#         db_recruiter = db.query(RecruiterModelDb).filter(RecruiterModelDb.email == login.email).first()

#         if db_recruiter is None or not pwd_context.verify(login.password, db_recruiter.password):
#             raise HTTPException(status_code=400, detail="Incorrect email or password")
        
#         db_company = db.query(CompanyModelDb).filter(CompanyModelDb.id == db_recruiter.company_id).first()

#         if db_company is None:
#             raise HTTPException(status_code=404, detail="Company not found")

#         access_token = create_jwt_token(data={
#             "id": db_recruiter.id,
#             "name": db_recruiter.name,
#             "company_id": db_recruiter.company_id,
#             "company_name": db_company.name,
#             "role": login.role,
#             "expires_delta": datetime.now(timezone.utc).timestamp() + 3600
#         })
    
#     if login.role == UserRoleSchema.candidate:
#         db_user = db.query(UserModelDb).filter(UserModelDb.email == login.email).first()

#         if db_user is None or not pwd_context.verify(login.password, db_user.password):
#             raise HTTPException(status_code=400, detail="Incorrect email or password")

#         access_token = create_jwt_token(data={
#             "id": db_user.id,
#             "name": db_user.name,
#             "role": login.role,
#             "expires_delta": datetime.now(timezone.utc).timestamp() + 3600
#         })

#     response = JSONResponse(content={
#         "message": "Login realizado"
#     })
#     response.set_cookie(key="access_token", value=access_token, httponly=True)
#     return response

@public_router.post("/predict", response_class=JSONResponse,
    summary="Predict candidate-job compatibility",
    description="""
    This endpoint receives data from a job and a candidate and returns a binary prediction (`0` or `1`) indicating whether the candidate is a good fit for the job, based on a machine learning model.

    It also returns the probability associated with the prediction.

    Authentication via Bearer Token is required.
    """,
    responses={
        200: {
            "description": "Prediction generated successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "predict": 1,
                        "proba": 0.8423
                    }
                }
            }
        },
        404: {
            "description": "Required data not found."
        },
        422: {
            "description": "Validation error. Provided filters are invalid or improperly formatted."
        },
        500: {
            "description": "Internal server error while generating prediction.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Error to find data: <error message>"
                    }
                }
            }
        }
    }
)
async def predict(predict: dict, db: Session = Depends(get_session_local)):
    try:
        if not predict or 'job' not in predict or 'user' not in predict:
            raise HTTPException(
                status_code=422,
                detail="Missing required fields: 'job' and 'user' must be provided."
            )
        
        client = MlflowClient()
        model_name = f"XGBoost_SMOTE_SPW{SCALE_POS_WEIGHT}"

        prod_version = client.get_model_version_by_alias(model_name, 'Production')
        model = get_or_load_model(model_name, prod_version.version)

        prospects = build_raw_candidate_dataset(predict['job'], predict['user'], {
            list(predict['job'].keys())[0]: {
                'prospects': [{
                    'codigo': list(predict['user'].keys())[0],
                    'situacao_candidado': None
                }]
            }
        })

        extracted_features = []
        for index, row in prospects.iterrows():
            features, target = process_features(row)
            extracted_features.append(features)

        X = np.array(extracted_features)
        probas = model.predict_proba(X)[:, 1]
        prediction = (probas >= THRESHOLD).astype(int)

        return JSONResponse(content={
            'predict': int(prediction[0]),
            'proba': float(probas)
        })
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error to find data: {str(e)}")