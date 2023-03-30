from sqlalchemy import Column, String

from ...schemas.user import UserRequestModel
from .base import Base


class UserModel(Base):
    __tablename__ = "users"

    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    phone_number = Column(String, nullable=False, index=True)
    country = Column(String, nullable=False)
    country_code = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    email = Column(String, nullable=True)

    @classmethod
    def create_from_model(cls, model: UserRequestModel):
        return cls(
            name=model.name,
            surname=model.surname,
            phone_number=model.phone_number,
            country=model.country,
            patronymic=model.patronymic,
            email=model.email,
            country_code=model.code_name
        )

    def dict(self):
        return {
            "name": self.name,
            "surname": self.surname,
            "phone_number": self.phone_number,
            "country": self.country,
            "patronymic": self.patronymic,
            "email": self.email,
        }
