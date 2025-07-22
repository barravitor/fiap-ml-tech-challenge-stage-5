# api/schemas/role_schemas.py
from enum import Enum

class UserRoleSchema(str, Enum):
    recruiter = "recruiter"
    candidate = "candidate"