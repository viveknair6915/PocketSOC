from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.auth.jwt_handler import verify_token
from backend.auth.rbac import Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)

def get_current_active_user(current_user: dict = Depends(get_current_user)):
    # Here check if user is active if needed
    return current_user

def require_role(role: Role):
    def role_checker(current_user: dict = Depends(get_current_active_user)):
        if current_user["role"] != role:
            raise HTTPException(status_code=403, detail="Operation not permitted")
        return current_user
    return role_checker
