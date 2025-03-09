from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    token: str

class ValidationResponse(BaseModel):
    valid: bool
    user: Optional[str] = None
    message: Optional[str] = None 