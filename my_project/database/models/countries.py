from sqlalchemy import Column, String

from ...schemas.country import ResponseCountryModel
from .base import Base


class CountryModel(Base):
    __tablename__ = "countries"

    name = Column(String, nullable=False, index=True)
    code_name = Column(String, nullable=False)

    @classmethod
    def create_from_model(cls, model: ResponseCountryModel):
        return cls(
            name=model.name,
            code_name=model.data.code,
        )

    def dict(self):
        return {
            "name": self.name,
            "code_name": self.code_name,
        }
