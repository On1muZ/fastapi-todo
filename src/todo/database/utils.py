from typing import Any, Sequence, Tuple
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from ..schemas import CreateToDo
from .models import ToDo
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, Row, delete, and_
from ..schemas import ToDo as BaseToDo

async def get_all_user_todos_from_db(user_id: UUID, session: AsyncSession) -> Sequence[Row[tuple[ToDo] | Any]]:
    query = select(ToDo).where(ToDo.user_id == user_id)
    data = await session.execute(query)
    return data.fetchall()


async def create_todo_in_database(todo: CreateToDo, user_id: UUID, session: AsyncSession):
    stmt = insert(ToDo).values(
        name=todo.name,
        text=todo.text,
        start_time=todo.time_to_start,
        finish_time=todo.time_to_finish,
        user_id=user_id
    )
    try:
        await session.execute(stmt)
    except:
        raise HTTPException(status_code=status.HTTP_500,
                            detail="Something went wrong!")
    else:
        await session.commit()


async def delete_todo_from_database(todo_id: UUID, session: AsyncSession):
    stmt = delete(ToDo).where(
        ToDo.id == todo_id
    )
    try:
        await session.execute(stmt)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500,
                            detail="Something went wrong!")
    else:
        await session.commit()


async def get_todo_by_id(todo_id: UUID, session: AsyncSession) -> ToDo:
    query = select(ToDo).where(ToDo.id == todo_id)
    data = await session.execute(query)
    return data.fetchone()[0]


async def update_todo_in_database(todo_id, todo: BaseToDo, session: AsyncSession):
    stmt = update(ToDo).where(ToDo.id == todo_id).values(
        name=todo.name,
        text=todo.text,
        start_time=todo.time_to_start,
        finish_time=todo.time_to_finish,
        is_finished=todo.completed
    )
    try:
        await session.execute(stmt)
    except:
        raise HTTPException(status_code=500)
    else:
        await session.commit()