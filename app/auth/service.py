"""
#   Copyright 2025 Matthew Ralston
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""
import os
from datetime import timedelta, datetime, timezone
from typing import Annotated
from passlib.context import CryptContext

from pydantic import EmailStr
from ulid import ulid

from fastapi import Depends
from sqlalchemy.orm import Session
import jwt
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

import logging

logger = logging.getLogger(__file__)


from . import model
from ..entities.user import User
from ..exceptions import AuthenticationError

SECRET_KEY = os.getenv("FASTAPI_SECRET_KEY")
if SECRET_KEY is None:
    raise EnvironmentError("No env variable named 'FASTAPI_SECRET_KEY'")

ALGORITHM = os.getenv("CRYPT_ALGO")
if ALGORITHM is None:
    raise EnvironmentError("No env variable named 'ALGORITHM'")

ACCESS_TOKEN_EXPIRES = 30# minutes

oauth2_pw_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verify_pw(pesswurd:str, heshhesh:str) -> bool:
    return bcrypt_context.verify(pesswurd, heshhesh)

def get_pw_hash(pesswurd: str) -> str:
    return bcrypt_context.hash(pesswurd)

def authenticate_user(email:EmailStr, pw: str, db: Session) -> User | bool:
    user = db.query(User).filter(User.email == email).first()
    if user is None or verify_pw(pw, user.password_hash) is False:
        logging.warning("Failed AUTH ATTEMPT for email : {0}".format(email))
        return False
    return user

def create_access_token(email: EmailStr, user_id: str, expires_delta: timedelta) -> str:
    encode = {
        'sub': email,
        'id': str(user_id),
        'exp': datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(encode, SECRET_KEY, algorithm=CRYPT_ALGO)

def verify_token(token: str) -> model.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[CRYPT_ALGO])
        user_id: str = payload.get('id')
        return model.TokenData(user_id=user_id)
    except jwt.PyJWTError as e:
        logging.warning("Invalid AUTH ATTEMPT could not verify token : {0}".format(token))
        logger.error(AuthenticationError("Couldn't verify JWT token"))
        raise e


def register_user(db: Session, register_user_request: model.RegisterUserRequest):
    try:
        create_user_model = User(id=ulid(),
                                 email=register_user_request.email,
                                 first_name=register_user_request.first_name,
                                 last_name=register_user_request.last_name,
                                 password_hash=get_pw_hash(register_user_request.password)
                                 )
        db.add(create_user_model)
        db.commit()
    except Exception as e:
        logger.error("Database exception on auth.service.register_user() : {0}".format(register_user_request))
        logger.error("Error: {0}".format(str(e)))
        raise e
            

def get_current_user(token: Annotated[str, Depends(oauth2_pw_bearer)]) -> model.TokenData:
    return verify_token(token)

CurrentUser = Annotated[model.TokenData, Depends(get_current_user)]

def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session) -> model.Token:
    # UHHH username?
    user = authenticate_user(form_data.email, form_data.password, db)
    if user is None:
        raise AuthenticationError("Login failed AUTH ATTEMPT for user with email {0}".format(form_data.email))
    token = create_access_token(user.email, user.id, timedelta(minutes=ACCESS_TOKEN - datetime.now(timezone.utc)))
    return model.Token(access_token=token, token_type='bearer')
                        
