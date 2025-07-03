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


from fastapi import HTTPException


class AuthenticationError(HTTPException):
    """
    Base exception for user authentication errors
    """
    pass


class UserNotFoundError(AuthenticationError):
    def __init__(self, user_id=None): # Is this a user id or an email address
        message = "User not found" if user_id is None else f"User not found with id {user_id}"
        super().__init__(status_code=404, detail=message)

class PasswordMismatchError(AuthenticationError):
    def __init__(self):
        super().__init__(status_code=400, detail="Password change rejected: passwords do not match")

class InvalidPasswordError(AuthenticationError):
    def __init__(self):
        super().__init__(status_code=401, detail="Password was invalid: Unauthorized")

