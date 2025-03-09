from fastapi import APIRouter, Depends
from typing import Dict, Any

from app.models.schemas import DataResponse
from app.core.auth import verify_token

router = APIRouter()

@router.get("/api/data", response_model=DataResponse)
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

@router.get("/api/health")
async def health_check():
    """Unprotected health check endpoint"""
    return {"status": "healthy"} 