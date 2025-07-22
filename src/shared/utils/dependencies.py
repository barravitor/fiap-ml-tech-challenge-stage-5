from fastapi import Request, HTTPException, status, Depends
from jose import JWTError
from .jwt_helper import verify_token
from ..db.database import get_session_local
from ..db.models.users_models import UserModelDb
from sqlalchemy.orm import Session

def get_current_user(request: Request, db: Session = Depends(get_session_local)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found")

    try:
        payload = verify_token(token)
        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token error")

        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid Token", headers={"WWW-Authenticate": "Bearer"})