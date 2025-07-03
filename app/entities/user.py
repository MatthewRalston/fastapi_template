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
from sqlalchemy import Column, String, DateTime#, Boolean, DateTime, ForeignKey, Enum
from pydantic import BaseModel, EmailStr


from ..database.core import Base

class UserModel(BaseModel):
    id: str = ulid()
    email: EmailStr
    first_name: str
    last_name: str
    password_hash: str



class User(Base):
    __tablename__ = "user"
    
    id = Column(String, primary_key=True, default=ulid)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    #create_date = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc()))
    #update_date = Column(DateTime, nullable=False))   

    
    def __repr__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"

    
