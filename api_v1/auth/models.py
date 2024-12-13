from models.base import Model, EmailStr


class TokenModel(Model):
    access_token: str
    token_type: str
    email: str


class TokenRequestModel(Model):
    email: EmailStr
