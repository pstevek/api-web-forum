from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

token_dependency = Annotated[str, Depends(oauth2_bearer)]
