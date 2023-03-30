import aiohttp
from loguru import logger

from my_project.database.db import async_session
from my_project.database.queries.country import (
    get_country_code,
    create_country, create_countries_if_not_exists,
)
from my_project.exceptions import NotFondCountryException
from my_project.schemas.country import ResponseCountriesModel
from my_project.settings import settings


async def get_code_name(country_name: str):
    # ищем в бд
    # отправляем запрос на получение
    # записываем результат в бд все что нашли, даже если это не то
    try:
        async with async_session() as session:
            return await get_country_code(country_name, session)
    except NotFondCountryException:
        logger.info(f'not found in cache {country_name=}')
        headers = {
            'Authorization': f'Token {settings.DADATA_API_KEY}',
            'Accept': 'application/json',
            'content-type': ' application/json',
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(
                    settings.DADATA_API_URL,
                    json={'query': country_name}
            ) as response:
                data = await response.json()
                result = ResponseCountriesModel.parse_obj(data)

                async with async_session() as session:
                    if len(result.suggestions) == 1:
                        # полное совпадение, сохраняем в кеш
                        model = await create_country(
                            result.suggestions[0], session
                        )
                        return model.code_name
                    elif len(result.suggestions) > 1:
                        # что то нашли, нужно это скешировать пригодиться
                        await create_countries_if_not_exists(
                            result.suggestions, session
                        )
                    raise
