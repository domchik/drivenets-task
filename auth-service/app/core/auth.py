import os
import jwt
import datetime
from fastapi import HTTPException, status
from typing import Dict, Any

# In a real application I would use environment variables for secrets
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')
# In a real application, store users in a database
USERS = {
    'user1': 'password1',
    'user2': 'password2'
}

def generate_token(username: str) -> str:
    """Generate a JWT token for the authenticated user"""
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow(),
        'sub': username
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_credentials(username: str, password: str) -> bool:
    """Verify user credentials"""
    return username in USERS and USERS[username] == password

def decode_token(token: str) -> Dict[str, Any]:
    """Decode and verify a JWT token"""
    try:
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

def extract_token_from_header(authorization: str) -> str:
    """Extract token from Authorization header"""
    if authorization.startswith('Bearer '):
        return authorization.split(' ')[1]
    return authorization 