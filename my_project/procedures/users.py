from my_project.database.db import async_session
from my_project.database.queries.user import (
    create_user, _get_user_by_phone,
    update_user, get_user_by_phone, delete_user,
)
from my_project.exceptions import NotFondUserException
from my_project.schemas.user import UserRequestModel, PhoneUserModel


async def save_user(model: UserRequestModel):
    await model.get_code_name()
    async with async_session() as session:
        try:
            await _get_user_by_phone(model.phone_number, session)
            await update_user(model, session)
        except NotFondUserException:
            await create_user(model, session)


async def get_user_data(model: PhoneUserModel):
    async with async_session() as session:
        return await get_user_by_phone(model, session)


async def delete_user_data(model: PhoneUserModel):
    async with async_session() as session:
        await delete_user(model, session)
        return model
