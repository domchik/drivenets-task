import os
import requests
from fastapi import FastAPI, Depends, HTTPException, Header, Request, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

app = FastAPI(title="Backend Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class Item(BaseModel):
    id: int
    name: str

class DataResponse(BaseModel):
    data: List[Item]

@app.get("/api/data", response_model=DataResponse)
async def get_data(_: Dict[str, Any] = Depends(verify_token)):
    """Example protected endpoint that returns data"""
    # This endpoint is protected and requires a valid JWT token
    return {
        "data": [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
            {"id": 3, "name": "Item 3"}
        ]
    }

@app.get("/api/health")
async def health_check():
    """Unprotected health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5001, reload=True)
