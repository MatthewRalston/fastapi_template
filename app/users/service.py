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


from ulid import ulid
from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import model

from ..entities.user import User
from ..exceptions import UserNotFoundError, InvalidPasswordError, PasswordMismatchError
from ..auth.service import verify_pw, get_pw_hash

import logging

logger = logging.getLogger(__file__)


def get_user_by_id(db: Session, user_id: str) -> model.UserResponse:
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        logger.warning(f"User not found given  id: {user_id}")
        raise UserNotFoundError(user_id)
    return user


def change_pw(db: Session, user_id: str, password_change: model.PasswordChange):
    try:
        user = get_user_by_id(db, user_id)
        # First make sure old password is valid
        if verify_pw(password_change.current_pw, user.password_hash) is False:
            logger.warning(f"Invalid password change produced for user '{user_id}'")
            raise InvalidPasswordError()
        # Now make sure passwords match internally to the change form
        elif password_change.new_pw != password_change.confirm_new_pw:
            raise PasswordMismatchError()
        # Now update
        user.password_hash = get_pw_hash(password_change.new_password)
        db.commit()
    except Exception as e:
        logger.error("Error during password change request for user {0}: {1}".format(user_id, str(user)))

        
        
