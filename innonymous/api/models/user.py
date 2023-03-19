from pydantic import BaseModel, Field, constr  # i hate constr


class User(BaseModel):
    uuid: str = Field(...)
    name: str = Field(...)


class UserCreateSchema(BaseModel):
    name: constr(regex=r"^[\w0-9][\w0-9\s\-_]{0,30}[\w0-9]$") = Field(...)  # type: ignore # noqa: PGH003
