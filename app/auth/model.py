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
from pydantic import BaseModel, EmailStr

class RegisterUserRequest(BaseModel):

    #id: str
    email: EmailStr
    first_name: str
    last_name: str
    password: str

    def __repr__(self) -> str:
        return f"{first_name} {last_name} <{email}>"
    

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str | None = None

    def get_ulid(self) -> str | None:
        if self.user_id is not None:
            return ulid(self.user_id) # Not sure this will work...
        return None

    
