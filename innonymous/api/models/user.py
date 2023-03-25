from datetime import datetime

from pydantic import BaseModel, Field, constr  # i hate constr

Base64String = str


class User(BaseModel):
    name: str = Field(...)
    password: str = Field(...)
    salt: str = Field(...)
    token_expires_at: datetime = Field(...)


class UserRegistrationForm(BaseModel):
    name: constr(regex=r"^[\w0-9][\w0-9\s\-_]{0,30}[\w0-9]$") = Field(...)  # type: ignore # noqa: PGH003


class UnconfirmedUserTokenPayload(BaseModel):
    name: str = Field(...)
    captcha_passphrase: str = Field(...)
    captcha_expires_at: datetime = Field(...)


class UserRegistrationResponse(BaseModel):
    pre_registration_token: str = Field(...)
    captcha_image: Base64String = Field(...)


class ConfirmUserRegistrationForm(BaseModel):
    pre_registration_token: str = Field(...)
    captcha_user_input: str = Field(...)
    password: str = Field(...)


class UserAccessTokenPayload(BaseModel):
    name: str = Field(...)
    expires_at: datetime = Field(...)


class UserAccess(BaseModel):
    name: str = Field(...)
    token: str = Field(...)
