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
from starlette import status
from fastapi import APIRouter



from ..database.core import DbSession
from . import model, service

from ..auth.service import CurrentUser

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



@router.get("/whoami", response_model=model.UserResponse)
def get_current_user(current_user: CurrentUser, db: DbSession):
    return service.get_user_by_id(db, current_user.get_ulid)


@router.put("/change_password", status_code=status.HTTP_200_OK)
def change_password(password_change: model.PasswordChange, db: DbSession, current_user: CurrentUser):

    service.change_password(db, current_user.get_ulid(), password_change)

    
