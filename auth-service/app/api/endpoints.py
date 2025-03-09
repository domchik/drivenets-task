from fastapi import APIRouter, Depends, HTTPException, Header, Request, status
from typing import Dict, Any, Optional

from app.models.schemas import LoginRequest, TokenResponse, ValidationResponse
from app.core.auth import generate_token, verify_credentials, decode_token, extract_token_from_header

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Login endpoint that returns a JWT token"""
    username = request.username
    password = request.password
    
    if verify_credentials(username, password):
        token = generate_token(username)
        return {"token": token}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
    )

@router.post("/validate", response_model=ValidationResponse)
async def validate_token(request: Request):
    """Endpoint to validate a JWT token"""
    authorization = request.headers.get('Authorization')
    
    if not authorization:
        return ValidationResponse(valid=False, message="Token is missing")
    
    try:
        token = extract_token_from_header(authorization)
        if not token:
            return ValidationResponse(valid=False, message="Token is missing")
            
        payload = decode_token(token)
        return ValidationResponse(valid=True, user=payload['sub'])
    except jwt.ExpiredSignatureError:
        return ValidationResponse(valid=False, message="Token has expired")
    except jwt.InvalidTokenError:
        return ValidationResponse(valid=False, message="Invalid token")
    except Exception as e:
        return ValidationResponse(valid=False, message=str(e))

async def verify_token(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """Verify JWT token from Authorization header"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing",
        )
    
    token = extract_token_from_header(authorization)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing",
        )
        
    return decode_token(token)

@router.get("/protected")
async def protected(payload: Dict[str, Any] = Depends(verify_token)):
    """Example of a protected endpoint"""
    return {"message": "This is a protected endpoint", "user": payload['sub']} 