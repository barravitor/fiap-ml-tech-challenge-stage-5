import httpx
import numpy as np
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from training.pipeline.build import candidate_dataset, candidate_geo_dataset, embed_dataset, feature_matrix
from training.preprocessing.geocode import generate_geocodes
from training.pipeline.train_storage import get_or_load_model
from shared.config import THRESHOLD, SCALE_POS_WEIGHT

public_router = APIRouter()

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
async def predict(predict: dict):
    try:
        if not predict or 'job' not in predict or 'user' not in predict:
            raise HTTPException(
                status_code=422,
                detail="Missing required fields: 'job' and 'user' must be provided."
            )

        model = get_or_load_model(f"XGBoost_SMOTE_SPW{SCALE_POS_WEIGHT}")

        df_raw = candidate_dataset(predict['job'], predict['user'], {
            list(predict['job'].keys())[0]: {
                'prospects': [{
                    'codigo': list(predict['user'].keys())[0],
                    'situacao_candidado': None
                }]
            }
        })

        df_geo = generate_geocodes(df_raw)
        df_cand_geo = candidate_geo_dataset(df_raw, df_geo)
        df_embed = embed_dataset(df_cand_geo)
        extracted_features = feature_matrix(df_embed)

        features = [{k: v for k, v in feature.items() if k != 'target'} for feature in extracted_features]
        print(len(features))

        X = np.array([np.concatenate(list(feature.values())) for feature in features], dtype=np.float32)
        print('X.shape', X)

        y_pred_proba = model.predict_proba(X)[:, 1]
        prediction = (y_pred_proba >= THRESHOLD).astype(int)

        return JSONResponse(content={
            'predict': int(prediction[0]),
            'proba': float(y_pred_proba)
        })
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error to find data: {str(e)}")