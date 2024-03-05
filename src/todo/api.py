from typing import Annotated
from uuid import UUID
from .schemas import ToDo as BaseToDo
from fastapi import Depends, HTTPException
from fastui.events import GoToEvent
from fastui.forms import fastui_form
from sqlalchemy.ext.asyncio import AsyncSession
from fastui import components as c
from auth.database.models import User
from auth.dependencies import get_current_user
from database import get_async_session
from .router import router
from .schemas import CreateToDo, DeleteToDo
from .database.utils import create_todo_in_database, delete_todo_from_database, get_todo_by_id, update_todo_in_database


@router.post("/create")
async def create_todo(todo: Annotated[CreateToDo, fastui_form(CreateToDo)],
                      user: User = Depends(get_current_user),
                      session: AsyncSession = Depends(get_async_session)):
    await create_todo_in_database(todo, user.id, session)
    return [c.FireEvent(event=GoToEvent(url='/todo/'))]


@router.post('/delete/{todo_id}')
async def delete_todo(todo_id: UUID,
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(get_current_user)):
    todo = await get_todo_by_id(todo_id, session)
    if user.id != todo.user_id:
        return HTTPException(status_code=403,
                             detail='Forbidden')
    await delete_todo_from_database(todo_id, session)
    return [c.FireEvent(event=GoToEvent(url='/todo/'))]


@router.post('/update/{todo_id}/')
async def update_todo(todo_id: UUID,
                      todo: Annotated[BaseToDo, fastui_form(BaseToDo)],
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(get_current_user)):
    print(todo, todo_id, user.id)
    todo_in_db = await get_todo_by_id(todo_id, session)
    if todo_in_db.user_id != user.id:
        return HTTPException(status_code=403,
                             detail="Forbidden")
    await update_todo_in_database(todo_id, todo, session)
    return [c.FireEvent(event=GoToEvent(url='/todo/'))]