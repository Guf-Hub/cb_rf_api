from pydantic import EmailStr
from models.base import Model


class TokenModel(Model):
    access_token: str
    token_type: str
    email: str


class TokenRequestModel(Model):
    email: EmailStr
