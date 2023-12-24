import os
import traceback
from typing import Annotated
from crud import get_model_by_id
from jose import jwt, JWTError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from schemas import UserCreate, UserResponse
from database import db_dependency, persist_db
from models import User
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
token_expiry = os.getenv("TOKEN_EXPIRY")

router = APIRouter(prefix="/auth", tags=["Authentication"])


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)

    return encoded_jwt


@router.post("/login")
def login(request: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    # Find user
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # Authenticate user
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token = create_access_token(
        data={"sub": user.username, 'id': user.id, 'role': user.role.name},
        expires_delta=timedelta(minutes=200)
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register(request: UserCreate, db: db_dependency):
    try:
        new_user = User(
            email=request.email,
            username=request.username,
            first_name=request.first_name,
            last_name=request.last_name,
            role_id=2,
            password=pwd_context.hash(request.password),
        )

        persist_db(db, new_user)

        response = jsonable_encoder(new_user)
        response['role'] = new_user.role.name

        return UserResponse(**response)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred while performing request :: {traceback.format_exc()}"
        )


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], db: db_dependency):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not authenticate user.')

        user = get_model_by_id(db, User, user_id)
        response = jsonable_encoder(user)
        response['role'] = user.role.name

        return UserResponse(**response)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please login again."
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error extracting user information :: {traceback.format_exc()}"
        )
