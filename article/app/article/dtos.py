from typing import Optional

from pydantic import BaseModel

from common.dtos import OrmBase


class ArticleDto(OrmBase):
    id: Optional[int]
    title: str
    author: str
    content: str


class UserDto(OrmBase):
    id: Optional[int]
    email: str


class UserEmailHistoryDto(OrmBase):
    id: Optional[int]
    user_email: str


class CreateUserEmailHistoryDto(UserEmailHistoryDto):
    user_id: int
