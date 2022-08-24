from typing import List

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


class UsersResponse(BaseModel):
    users: List[User]

    class Config:
        orm_mode = True
