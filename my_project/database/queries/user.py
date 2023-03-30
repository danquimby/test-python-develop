from loguru import logger
from sqlalchemy import delete, select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from my_project.database.models.users import UserModel
from my_project.exceptions import NotFondUserException
from my_project.schemas.user import PhoneUserModel, UserRequestModel


async def create_user(
    model: UserRequestModel,
    db_session: AsyncSession,
) -> UserRequestModel:
    logger.info(f'Create model {model.dict()}')
    user_model = UserModel.create_from_model(model)
    db_session.add(user_model)
    await db_session.commit()
    await db_session.flush()
    return UserRequestModel.parse_obj(user_model.dict())


async def update_user(
    model: UserRequestModel,
    db_session: AsyncSession,
) -> UserRequestModel:
    logger.info(f'Update model {model.dict()}')
    await db_session.execute(
        update(UserModel)
        .where(UserModel.phone_number == model.phone_number)
        .values(
            name=model.name,
            surname=model.surname,
            country=model.country,
            patronymic=model.patronymic,
            email=model.email
        )
    )
    await db_session.commit()
    await db_session.flush()
    return model


async def get_user_by_phone(
    model: PhoneUserModel,
    db_session: AsyncSession,
) -> UserRequestModel:
    result = await _get_user_by_phone(model.phone_number, db_session)
    logger.info(f'Get model result: {result=}')
    model = list(result)[0]
    return UserRequestModel.parse_obj(model.dict())


async def delete_user(
    model: PhoneUserModel,
    db_session: AsyncSession,
) -> None:
    logger.info(
        f"Delete model {model.dict()}"
    )
    await _get_user_by_phone(model.phone_number, db_session)
    await db_session.execute(
        delete(UserModel).where(
            UserModel.phone_number == model.phone_number
        )
    )
    await db_session.commit()


async def _get_user_by_phone(
    phone_number: str,
    db_session: AsyncSession,
) -> dict:
    res: Result = await db_session.execute(
        select(UserModel).where(
            UserModel.phone_number == phone_number
        )
    )
    result = res.fetchone()
    if result is None:
        raise NotFondUserException(phone_number)
    return result
