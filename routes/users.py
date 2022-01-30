from fastapi import APIRouter, Depends
from fastapi import HTTPException
from datetime import datetime

from schemas import schema as _schm
from config import settings
from services import services as _srvc

router = APIRouter()

database = settings.get_db_users()


@router.get("/me/", response_model=_schm.User, tags=["Users"])
async def read_users_me(current_user: _schm.User = Depends(_srvc.get_current_user)):
    return current_user


@router.get("/my_project/", tags=["Users"])
async def read_own_items(current_user: _schm.User = Depends(_srvc.get_current_user)):
    return [{"item_id": "Foo", "owner": current_user["email"]}]


@router.post("/register/", response_model=_schm.User, tags=["Users"])
async def register_user(new_user: _schm.UserRegister):

    exception = HTTPException(
        status_code=400, detail="the email is already registered in the application."
    )

    user = await database["users"].find_one({"_id": new_user.email})

    if user:
        raise exception
    else:
        hashed_password = _srvc.get_password_hash(new_user.password)
        user_obj = dict(new_user)
        user_obj["password"] = hashed_password
        user_obj["register_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_obj.update({"_id": new_user.email})
        inserted_user = await database["users"].insert_one(user_obj)
        new_user = await database["users"].find_one({"_id": inserted_user.inserted_id})

    return new_user
