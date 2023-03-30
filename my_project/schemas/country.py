from typing import List

from pydantic import BaseModel, Field


class ResponseCountryDataModel(BaseModel):
    code: str


class ResponseCountryModel(BaseModel):
    name: str = Field(alias='value')
    data: ResponseCountryDataModel


class ResponseCountriesModel(BaseModel):
    suggestions: List[ResponseCountryModel] = Field(default_factory=list)
