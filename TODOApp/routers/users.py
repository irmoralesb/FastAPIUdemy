from fastapi import Depends, HTTPException, APIRouter
from ..models import Users
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from .auth import get_current_user, hash_password, authenticate_user
from pydantic import BaseModel, Field
router = APIRouter(
    prefix='/users',
    tags=['users']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class UserVerification(BaseModel):
    old_password:str
    new_password: str = Field(min_length=6)
    new_password_repeat: str = Field

@router.get("/user_info", status_code=status.HTTP_200_OK)
async def get_user_info(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization failed')

    return db.query(Users).filter(Users.id == user.get("id")).first()


@router.put("/change_password", status_code=status.HTTP_200_OK)
async def change_password(user: user_dependency, db: db_dependency,user_verification: UserVerification ):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization failed')

    if user_verification.new_password != user_verification.new_password_repeat:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New Password does not match")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if authenticate_user(user.get("username"), user_verification.old_password, db):
        user_model.hashed_password = hash_password(user_verification.new_password)
        db.commit()
        return

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password!")

# @router.put('phonenumber/{phone_number}', status_code=status.HTTP_204_NO_CONTENT)
# async def change_phone_number(user:user_dependency, db: db_dependency, phone_number: str):
#
#     if user is None:
#         raise HTTPException(status_code=401, detail="Authentication failed")
#
#     user_model = db.query(Users).filter(Users.id == user.get("id")).first()
#     user_model.phone_number = phone_number
#     db.commit()