# api/schemas/token_schemas.py
from pydantic import BaseModel

class TokenSchema(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True
