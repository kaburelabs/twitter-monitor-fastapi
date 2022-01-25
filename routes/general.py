from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from config import settings

from datetime import datetime, timedelta

from schemas import schema as _schm
from services import services as _srvc

router = APIRouter()

_, _, ACCESS_TOKEN_EXPIRE_MINUTES = settings.settings()


@router.get("/", tags=["Root"])
async def root():

    return {
        "status": "running",
        "message": "Welcome to the cardano NFTs monitor API. Go to /docs path to see all the endpoints avaialable.",
    }


@router.post("/token", response_model=_schm.Token, tags=["Root"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    user = await _srvc.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = _srvc.create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
