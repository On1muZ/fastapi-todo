from typing import Annotated
from fastapi import Depends, HTTPException, status, Response
from fastui.events import GoToEvent
from fastui.forms import fastui_form
from sqlalchemy.ext.asyncio import AsyncSession
from .router import router
from .schemas import CreateUser, LoginUser
from auth.database.utils import save_user, get_user_by_username
from database import get_async_session
from .utils import verify_password, sign_jwt
from fastui import components as c


@router.post('/sign_up')
async def sign_up_user(user: Annotated[CreateUser, fastui_form(CreateUser)],
                       session: AsyncSession = Depends(get_async_session)):
    if user.confirm_password == user.password:
        await save_user(username=user.username,
                        password=str(user.confirm_password),
                        session=session)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Password's does not equal")
    return [c.FireEvent(event=GoToEvent(url='/auth'))]


@router.post('/sign_in')
async def sign_in_user(response: Response,
                       user: Annotated[LoginUser, fastui_form(LoginUser)],
                       session: AsyncSession = Depends(get_async_session)):
    user_from_db = await get_user_by_username(user.username, session)
    if user_from_db is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect data")
    if verify_password(str(user.password), user_from_db.hashed_password):
        response.set_cookie(key="access_token",
                            value=sign_jwt(username=user.username,
                                           user_id=user_from_db.id),
                            httponly=True
                            )
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect data")
    return [c.FireEvent(event=GoToEvent(url='/todo/'))]


@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie("access_token")
    return [c.FireEvent(event=GoToEvent(url='/auth/'))]