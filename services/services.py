from config import settings
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from schemas import schema as _schemas
from services import update_twitter

SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES = settings.settings()
database = settings.get_db()
projects_db = settings.get_db_projects()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(username: str):
    user = await database["users"].find_one({"_id": username})
    if user:
        return user


async def authenticate_user(username: str, password: str):
    user = await database["users"].find_one({"_id": username})

    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = _schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = await get_user(username=token_data.username)

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: _schemas.User = Depends(get_current_user),
):
    if "disabled" in current_user:
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def update_project(conn, project, values):

    proj = await conn["projects_card_data"].find_one({"project_name": project})
    values["oficial_drop"] = datetime.fromordinal(values["oficial_drop"].toordinal())
    if proj:
        await conn["projects_card_data"].update_one(
            {"project_name": project}, {"$set": values}
        )
        proj = await conn["projects_card_data"].find_one({"project_name": project})
        return proj
    else:
        raise HTTPException(status_code=400, detail="Inactive user")
