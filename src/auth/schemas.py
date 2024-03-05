from pydantic import BaseModel, SecretStr


class CreateUser(BaseModel):
    username: str
    password: SecretStr
    confirm_password: SecretStr


class LoginUser(BaseModel):
    username: str
    password: SecretStr