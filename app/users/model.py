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

from pydantic import BaseModel, EmailStr
from ulid import ulid

from datetime import datetime

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    first_name: str
    last_name: str

class PasswordChange(BaseModel):
    current_pw: str
    new_pw: str
    confirm_new_pw: str

