from sqlmodel import SQLModel, Field
from pydantic import EmailStr


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)