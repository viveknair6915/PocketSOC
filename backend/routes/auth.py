from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from backend.auth.jwt_handler import create_access_token
from backend.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Demostration login. In production, verify against DB
    # We accept: admin/admin, agent/agent, analyst/analyst for demo
    
    if form_data.username == "admin" and form_data.password == "admin":
        user_role = "admin"
    elif form_data.username == "analyst" and form_data.password == "analyst":
        user_role = "analyst"
    elif form_data.username == "agent" and form_data.password == "agent":
        user_role = "agent"
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": form_data.username, "role": user_role}
    )
    return {"access_token": access_token, "token_type": "bearer"}
