from datetime import timedelta, datetime, timezone
from http.client import HTTPException
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = 'a4018bb2f6d60ef6948ae8e53afd371840932c182668d703a53951ddbd53206a'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class CreateUserRequest(BaseModel):
    username : str
    email : str
    first_name : str
    last_name : str
    password : str
    role : str


class Token(BaseModel):
    access_token : str
    token_type : str



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

#Auth processing
def authenticate_user(username:str,password:str,db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return  user

#CREATE JWT TOKEN
def create_access_token(username: str, user_id : int, expire_delta : timedelta):
    encode = {'sub' : username, 'id' : user_id}
    expires = datetime.now(timezone.utc) + expire_delta
    encode.update({'exp' : expires})
    return jwt.encode(encode, SECRET_KEY, algorithm= ALGORITHM)

#GET CURRENT USER (DECODE)
async def get_current_user(token : Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        username : str = payload.get('sub')
        user_id : int = payload.get('id')
        if username is None or user_id is None:
            print("user not found")
            raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail='Could not validate')
        return {'username': username, 'id':user_id}
    except JWTError:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                        detail= "not validate")



#******* Create User
@router.post('/', status_code = status.HTTP_201_CREATED)
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
@router.post('/token', response_model=Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],
                                 db: db_dependency):

    user = authenticate_user(form_data.username,form_data.password,db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate')

    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {'access_token' : token, 'token_type': 'bearer'}