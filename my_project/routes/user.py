from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from my_project.exceptions import NotFondUserException, NotFondCountryException
from my_project.procedures.users import (
    save_user, get_user_data,
    delete_user_data,
)
from my_project.schemas.user import PhoneUserModel, UserRequestModel

router = APIRouter()


@router.post("/save_user_data")
async def post_request_to_save_user_data(model: UserRequestModel):
    try:
        return await save_user(model)
    except NotFondCountryException as e:
        return HTTPException(
            status_code=404,
            detail=str(e)
        )
    except KeyError as e:
        return HTTPException(status_code=500, detail=str(e))


@router.post("/get_user_data")
async def post_request_to_get_user_data(request: PhoneUserModel):
    try:
        await get_user_data(request)
    except NotFondUserException as e:
        return HTTPException(
            status_code=404,
            detail=str(e)
        )
    except KeyError as e:
        return HTTPException(status_code=500, detail=str(e))


@router.post("/delete_user_data")
async def post_request_to_delete_user_data(request: PhoneUserModel):
    try:
        return await delete_user_data(request)
    except NotFondUserException as e:
        return HTTPException(
            status_code=404,
            detail=str(e)
        )
    except KeyError as e:
        return HTTPException(status_code=500, detail=str(e))
