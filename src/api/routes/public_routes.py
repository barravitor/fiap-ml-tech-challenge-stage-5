# api/routes/public_routes.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..schemas.index_schemas import LoginSchema, TokenSchema, UserRoleSchema, ChatMessageSchema
from ...shared.db.models.index_models import RecruiterModelDb, CompanyModelDb, UserModelDb
from ...shared.db.database import get_session_local
from datetime import datetime, timezone
from passlib.context import CryptContext
from shared.utils.jwt_helper import create_jwt_token

public_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@public_router.post("/auth/login", response_model=TokenSchema,
    responses={
        200: {
            "description": "Returns an access token.",
            "content": {
                "application/json": {
                    "schema": TokenSchema.model_json_schema(),
                    "example": {
                        "access_token": "token_jwt_generated",
                        "token_type": "bearer"
                    }
                }
            }
        },
        400: {
            "description": "Bad Request.",
            "content": {
                "application/json": {
                    "examples": {
                        "incorrect_email_or_password": {
                            "summary": "Incorrect email or password",
                            "value": {
                                "detail": "Incorrect email or password"
                            }
                        }
                    }
                }
            }
        }
    }
)
def login(login: LoginSchema, db: Session = Depends(get_session_local)):
    """
    Login the recruiter into the platform.
    
    - **Return**: An access token on success.

    ## Possible Errors:
    - **400 Bad Request**: If are incorrect email or password.
    """

    access_token: str

    if login.role == UserRoleSchema.recruiter:
        db_recruiter = db.query(RecruiterModelDb).filter(RecruiterModelDb.email == login.email).first()

        if db_recruiter is None or not pwd_context.verify(login.password, db_recruiter.password):
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        
        db_company = db.query(CompanyModelDb).filter(CompanyModelDb.id == db_recruiter.company_id).first()

        if db_company is None:
            raise HTTPException(status_code=404, detail="Company not found")

        access_token = create_jwt_token(data={
            "id": db_recruiter.id,
            "name": db_recruiter.name,
            "company_id": db_recruiter.company_id,
            "company_name": db_company.name,
            "role": login.role,
            "expires_delta": datetime.now(timezone.utc).timestamp() + 3600
        })
    
    if login.role == UserRoleSchema.candidate:
        db_user = db.query(UserModelDb).filter(UserModelDb.email == login.email).first()

        if db_user is None or not pwd_context.verify(login.password, db_user.password):
            raise HTTPException(status_code=400, detail="Incorrect email or password")

        access_token = create_jwt_token(data={
            "id": db_user.id,
            "name": db_user.name,
            "role": login.role,
            "expires_delta": datetime.now(timezone.utc).timestamp() + 3600
        })

    response = JSONResponse(content={
        "message": "Login realizado"
    })
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

    # return {
    #     "access_token": access_token,
    #     "role": login.role,
    #     "token_type": "bearer"
    # }
