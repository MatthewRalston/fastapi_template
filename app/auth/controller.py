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
from typing import Annotated, List

from starlette import status
from fastapi import Request, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm


from ..database.core import DbSession
from . import model, service
from ..entities.user import User, UserModel

#from ..rate_limiter import limiter

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)

#@limiter.limit("1/day")
@router.post('/auth/register', status_code=status.HTTP_201_CREATED)
async def register_user(request: Request, register_user_request: model.RegisterUserRequest, db: DbSession):
    service.register_user(db, register_user_request)

@router.post("/token", response_model=model.Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession) -> model.Token:
    return service.login_for_access_token(form_data, db)


@router.get("/user/all", response_model=list[UserModel])
def get_users(db: DbSession):
    users = db.query(User).all()
    return users
