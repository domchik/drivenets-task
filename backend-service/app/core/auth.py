import os
import requests
from fastapi import HTTPException, Header, status
from typing import Dict, Any, Optional

# In a real application I would use environment variables for service URLs
AUTH_SERVICE_URL = os.environ.get('AUTH_SERVICE_URL', 'http://auth-service:5000')

async def verify_token(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """Middleware to validate JWT tokens with the auth service"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing",
        )
    
    # Forward the token to the auth service for validation
    try:
        response = requests.post(
            f"{AUTH_SERVICE_URL}/validate",
            headers={'Authorization': authorization}
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )
            
        result = response.json()
        if not result.get('valid', False):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=result.get('message', 'Invalid token'),
            )
            
        # Token is valid, return the user info
        return {"user": result.get('user')}
    except requests.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error validating token: {str(e)}",
        ) 