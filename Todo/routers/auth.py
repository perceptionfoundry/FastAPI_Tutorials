from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.util import deprecated

from models import Users
from passlib.context import CryptContext

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class CreateUserRequest(BaseModel):
    username : str
    email : str
    first_name : str
    last_name : str
    password : str
    role : str





@router.post('/auth/')
async def create_user(create_request : CreateUserRequest):

    create_user_model = Users(
        email = create_request.email,
        username = create_request.username,
        first_name = create_request.first_name,
        last_name = create_request.last_name,
        hashed_password = bcrypt_context.hash(create_request.password),
        role = create_request.role,
        is_active = True
    )

    return create_user_model