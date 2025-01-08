from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class CreateUserRequest(BaseModel):
    username : str
    email : str
    first_name : str
    last_name : str
    password : str
    role : str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

#Auth processing
def authenticate_user(username:str,
                      password:str,
                      db):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return  True

#******* Create User
@router.post('/auth/', status_code = status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_request : CreateUserRequest):

    create_user_model = Users(
        email = create_request.email,
        username = create_request.username,
        first_name = create_request.first_name,
        last_name = create_request.last_name,
        hashed_password = bcrypt_context.hash(create_request.password),
        role = create_request.role,
        is_active = True
    )

    db.add(create_user_model)
    db.commit()

#************** Create Token on Access
@router.post('/tokens')
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],
                                 db: db_dependency):

    user = authenticate_user(form_data.username,
                             form_data.password,
                             db)

    if not user:
        return "failed auth"
    return "success auth"