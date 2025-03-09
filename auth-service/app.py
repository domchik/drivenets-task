import os
import jwt
import datetime
from fastapi import FastAPI, Depends, HTTPException, Header, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.main import app

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In a real application I would use environment variables for secrets
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')
# In a real application, store users in a database
USERS = {
    'user1': 'password1',
    'user2': 'password2'
}

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    token: str

class ValidationResponse(BaseModel):
    valid: bool
    user: Optional[str] = None
    message: Optional[str] = None

def generate_token(username: str) -> str:
    """Generate a JWT token for the authenticated user"""
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow(),
        'sub': username
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

async def verify_token(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """Verify JWT token from Authorization header"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing",
        )
    
    try:
        token = None
        if authorization.startswith('Bearer '):
            token = authorization.split(' ')[1]
        else:
            token = authorization
            
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is missing",
            )
            
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

@app.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Login endpoint that returns a JWT token"""
    username = request.username
    password = request.password
    
    if username in USERS and USERS[username] == password:
        token = generate_token(username)
        return {"token": token}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
    )

@app.post("/validate", response_model=ValidationResponse)
async def validate_token(request: Request):
    """Endpoint to validate a JWT token"""
    authorization = request.headers.get('Authorization')
    
    if not authorization:
        return ValidationResponse(valid=False, message="Token is missing")
    
    try:
        token = None
        if authorization.startswith('Bearer '):
            token = authorization.split(' ')[1]
        else:
            token = authorization
            
        if not token:
            return ValidationResponse(valid=False, message="Token is missing")
            
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return ValidationResponse(valid=True, user=payload['sub'])
    except jwt.ExpiredSignatureError:
        return ValidationResponse(valid=False, message="Token has expired")
    except jwt.InvalidTokenError:
        return ValidationResponse(valid=False, message="Invalid token")

@app.get("/protected")
async def protected(payload: Dict[str, Any] = Depends(verify_token)):
    """Example of a protected endpoint"""
    return {"message": "This is a protected endpoint", "user": payload['sub']}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
