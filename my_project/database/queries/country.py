import asyncio
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from my_project.database.models.countries import CountryModel
from my_project.exceptions import NotFondCountryException
from my_project.schemas.country import ResponseCountryModel


async def create_country(
    model: ResponseCountryModel,
    db_session: AsyncSession,
) -> CountryModel:
    user_model = CountryModel.create_from_model(model)
    db_session.add(user_model)
    await db_session.commit()
    await db_session.flush()
    return user_model


async def get_country_code(
    name: str,
    db_session: AsyncSession,
) -> Optional[str]:
    result: Result = await db_session.execute(
        select(CountryModel).where(
            CountryModel.name == name
        )
    )
    result = result.fetchone()
    if result is None:
        raise NotFondCountryException(name)
    return list(result)[0].code_name


async def create_country_if_not_exists(
    model: ResponseCountryModel,
    db_session: AsyncSession,
):
    try:
        await get_country_code(model.name, db_session)
    except NotFondCountryException:
        await create_country(model, db_session)


async def create_countries_if_not_exists(
    models: List[ResponseCountryModel],
    db_session: AsyncSession,
):
    await asyncio.gather(
        *(create_country_if_not_exists(model, db_session) for model in models)
    )
