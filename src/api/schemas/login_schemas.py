# api/schemas/user_login_schemas.py
from pydantic import BaseModel, EmailStr, Field
from .role_schemas import UserRoleSchema

class LoginSchema(BaseModel):
    email: EmailStr = Field(..., example="youremail@example.com", description="Your valid email")
    password: str = Field(..., example="yourpassword", description="The user's password.")
    role: UserRoleSchema

    class Config:
        from_attributes = True