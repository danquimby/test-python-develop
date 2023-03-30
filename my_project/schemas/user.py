import re
from typing import Optional

from loguru import logger
from pydantic import BaseModel, EmailStr, Field, validate_email, validator

from my_project.procedures.countries import get_code_name


class PhoneUserModel(BaseModel):
    phone_number: str = Field(description='номер телефона')

    @validator("phone_number")
    def phone_validation(cls, v):
        logger.debug(f"phone in 2 validator:{v}")
        regex = r"^(\+)[7][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v


class CountryMixinModel(BaseModel):
    country: str = Field(description='Страна пользователя')
    code_name: Optional[str] = Field(description='Код страны')

    async def get_code_name(self):
        result = await get_code_name(self.country)
        self.code_name = result


class UserRequestModel(PhoneUserModel, CountryMixinModel):
    name: str = Field(description='Имя пользователя')
    surname: str = Field(description='Фамилия пользователя')
    patronymic: Optional[str] = Field(description='Отчетсво пользователя')
    email: Optional[EmailStr] = Field(description='Почта пользователя')

    @validator("name")
    def name_validation(cls, v):
        regex = r"[а-яёА-ЯЁ -]"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Только кирилица")
        if v and len(v) > 50:
            raise ValueError("50 символов максимум")
        return v

    @validator("surname")
    def surname_validation(cls, v):
        regex = r"[а-яёА-ЯЁ -]"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Только кирилица")
        if v and len(v) > 50:
            raise ValueError("50 символов максимум")
        return v

    @validator("patronymic")
    def patronymic_validation(cls, v):
        if v:
            regex = r"[а-яёА-ЯЁ -]"
            if v and not re.search(regex, v, re.I):
                raise ValueError("Только кирилица")
            return v

    @validator("email")
    def email_validation(cls, v):
        if v:
            validate_email(v)
        return v


class UserResponseModel(UserRequestModel):
    pass


class UserSearchRequestModel(PhoneUserModel):
    pass
