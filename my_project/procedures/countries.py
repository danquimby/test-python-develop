from typing import List

import aiohttp
from pydantic import AnyUrl

from my_project.database.db import async_session
from my_project.database.queries.country import (
    get_country_code,
    create_country, create_countries_if_not_exists,
)
from my_project.exceptions import NotFondCountryException
from my_project.schemas.country import (
    ResponseCountriesModel,
    ResponseCountryModel,
)
from my_project.settings import settings


class DaDataService():
    url: AnyUrl = settings.DADATA_API_URL
    api_key: str = settings.DADATA_API_KEY

    async def get_code_name(self, country_name: str):
        async with async_session() as session:
            try:
                return await get_country_code(country_name, session)
            except NotFondCountryException:
                result = await self.get_country_from_service(country_name)
                if len(result) == 1:
                    # полное совпадение, сохраняем в кеш
                    model = await create_country(
                        result[0], session
                    )
                    return model.code_name
                elif len(result) > 1:
                    # что то нашли, нужно это скешировать пригодиться
                    await create_countries_if_not_exists(
                        result, session
                    )
                raise

    async def get_country_from_service(self, country_name: str) \
            -> List[ResponseCountryModel]:
        headers = {
            'Authorization': f'Token {self.api_key}',
            'Accept': 'application/json',
            'content-type': ' application/json',
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(
                    self.url,
                    json={'query': country_name}
            ) as response:
                data = await response.json()
                return ResponseCountriesModel.parse_obj(data).suggestions


dadata_service: DaDataService = DaDataService()
