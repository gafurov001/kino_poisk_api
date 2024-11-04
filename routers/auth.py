from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from models import User
from schemas import UserAuth, UserOut, TokenSchema
from utils import get_current_user
from utils import get_hashed_password, verify_password, create_access_token, create_refresh_token

auth_router = APIRouter()


@auth_router.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    user = await User.get_by_email(data.email)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = await User.create(name=data.name, username=data.username, password=get_hashed_password(data.password),
                       email=data.email)
    return user


@auth_router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.get_by_username(form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }



@auth_router.get('/profile', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: User = Depends(get_current_user)):
    return user