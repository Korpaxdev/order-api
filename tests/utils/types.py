from typing import TypedDict


class UserType(TypedDict):
    username: str
    email: str
    password: str


class UserTokenType(TypedDict):
    username: str
    password: str
