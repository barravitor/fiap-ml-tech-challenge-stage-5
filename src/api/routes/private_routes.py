# api/routes/private_routes.py
import os
import pandas as pd
import httpx
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import desc
from shared.utils.dependencies import get_current_user
from shared.db.models.index_models import JobModelDb
from sqlalchemy.orm import Session
from shared.db.database import get_session_local
from training.pipeline.feature_engineering import process_features
from api.schemas.index_schemas import JobSchema, BasicInformationSchema, ProfileSchema

from training.data.build_dataset import build_raw_candidate_dataset
from training.pipeline.train_storage import load_scaler, load_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

private_router = APIRouter()

@private_router.get("/users/me", response_class=JSONResponse,
    responses={
        200: {
            "description": "CSV file with exportation data.",
            "content": {
                "text/csv": {
                    "example": "category,date\nVinhos de mesa,1970-12-21\nVinhos de mesa,1971-12-21\n"
                }
            }
        },
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_token": {
                            "summary": "Unauthorized",
                            "value": {
                                "detail": "Unauthorized: Invalid Token"
                            }
                        },
                        "not_authenticated": {
                            "summary": "Unauthorized",
                            "value": {
                                "detail": "Not authenticated"
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "Data not found."
        },
        422: {
            "description": "Unprocessable Entity. Validation error in provided filters."
        },
    }
)
async def get_users_me(current_user: dict = Depends(get_current_user), db: Session = Depends(get_session_local)):
    """
    Retrieve exportation data in CSV format.

    - **Return**: A CSV file with exportation data.

    ## Possible Errors:
    - **401 Unauthorized**: If the JWT token is not provided or is invalid.
    - **422 Unprocessable Entity**: If the provided filter data does not pass validation.
    """
    try:
        return JSONResponse(content={"user": current_user})
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error to find data: {str(e)}")

@private_router.get("/recruiters/jobs", response_model=list[JobSchema],
    responses={
        200: {
            "description": "List of jobs",
            "content": {
                "application/json": {
                    "schema": JobSchema.model_json_schema()
                }
            }
        },
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_token": {
                            "summary": "Unauthorized",
                            "value": {
                                "detail": "Unauthorized: Invalid Token"
                            }
                        },
                        "not_authenticated": {
                            "summary": "Unauthorized",
                            "value": {
                                "detail": "Not authenticated"
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "Data not found."
        },
        422: {
            "description": "Unprocessable Entity. Validation error in provided filters."
        },
    }
)
async def get_jobs(current_user: dict = Depends(get_current_user), db: Session = Depends(get_session_local)):
    """
    Retrieve exportation data in CSV format.

    - **Return**: A CSV file with exportation data.

    ## Possible Errors:
    - **401 Unauthorized**: If the JWT token is not provided or is invalid.
    - **422 Unprocessable Entity**: If the provided filter data does not pass validation.
    """
    try:
        jobs = (
            db.query(JobModelDb)
            .filter(JobModelDb.company_id == current_user["company_id"])
            .order_by(desc(JobModelDb.created_at))
            .limit(10)
            .all()
        )

        result = []
        for job in jobs:
            basic = BasicInformationSchema(
                job_external_id=job.job_external_id,
                job_title=job.job_title,
                created_at=job.created_at
            )
            profile = ProfileSchema(
                country=job.country,
                state=job.state,
                city=job.city,
                neighborhood=job.neighborhood
            )
            result.append(JobSchema(
                id=job.id,
                basicInformation=basic,
                profile=profile
            ))

        return result
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error to find data: {str(e)}")

@private_router.post("/recruiters/jobs", response_class=JSONResponse,
    responses={
        200: {
            "description": "CSV file with exportation data.",
            "content": {
                "text/csv": {
                    "example": "category,date\nVinhos de mesa,1970-12-21\nVinhos de mesa,1971-12-21\n"
                }
            }
        },
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_token": {
                            "summary": "Unauthorized",
                            "value": {
                                "detail": "Unauthorized: Invalid Token"
                            }
                        },
                        "not_authenticated": {
                            "summary": "Unauthorized",
                            "value": {
                                "detail": "Not authenticated"
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "Data not found."
        },
        422: {
            "description": "Unprocessable Entity. Validation error in provided filters."
        },
    }
)
async def post_jobs(job: JobSchema, current_user: dict = Depends(get_current_user), db: Session = Depends(get_session_local)):
    """
    Retrieve exportation data in CSV format.

    - **Return**: A CSV file with exportation data.

    ## Possible Errors:
    - **401 Unauthorized**: If the JWT token is not provided or is invalid.
    - **422 Unprocessable Entity**: If the provided filter data does not pass validation.
    """
    try:
        new_job = JobModelDb(
            job_external_id=job.basicInformation.job_external_id,
            job_title=job.basicInformation.job_title,
            company_id=current_user["company_id"],
            country=job.profile.country,
            state=job.profile.state,
            city=job.profile.city,
            neighborhood=job.profile.neighborhood,
            created_at=datetime.now(timezone.utc)
        )
        db.add(new_job)
        db.commit()
        db.refresh(new_job)

        return JSONResponse(content={
            "job_id": new_job.id,
            "applied_url": "http://localhost:8000/public/jobs/{new_job.id}"
        })
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error to find data: {str(e)}")
    
@private_router.post("/predict", response_class=JSONResponse,
    responses={
        200: {
            "description": "CSV file with exportation data.",
            "content": {
                "text/csv": {
                    "example": "category,date\nVinhos de mesa,1970-12-21\nVinhos de mesa,1971-12-21\n"
                }
            }
        },
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_token": {
                            "summary": "Unauthorized",
                            "value": {
                                "detail": "Unauthorized: Invalid Token"
                            }
                        },
                        "not_authenticated": {
                            "summary": "Unauthorized",
                            "value": {
                                "detail": "Not authenticated"
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "Data not found."
        },
        422: {
            "description": "Unprocessable Entity. Validation error in provided filters."
        },
    }
)
async def predict(predict: dict, current_user: dict = Depends(get_current_user), db: Session = Depends(get_session_local)):
    try:
        print(list(predict['user'].keys())[0])

        data = build_raw_candidate_dataset(predict['job'], predict['user'], {
            list(predict['job'].keys())[0]: {
                'prospects': [{
                    'codigo': list(predict['user'].keys())[0],
                    'situacao_candidado': None
                }]
            }
        })

        extracted_features = []
        for index, row in data.iterrows():
            features = process_features(row)
            extracted_features.append(features)

        df_features = pd.DataFrame(extracted_features)
        print(df_features.values)
        df_features.fillna(0, inplace=True)

        scaler = load_scaler(f"{os.path.join(BASE_DIR, '..', '..', 'training', 'data', 'processed')}/scaler.pkl")
        model = load_model(f"{os.path.join(BASE_DIR, '..', '..', 'training', 'data', 'processed')}/model.pkl")

        X_scaled = scaler.transform(df_features.values)

        prediction = model.predict(X_scaled)

        return JSONResponse(content={
            'predict': int(prediction[0])
        })
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error to find data: {str(e)}")