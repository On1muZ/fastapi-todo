from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from .database.models import ToDo
from fastapi import Depends
from auth.dependencies import get_current_user
from auth.database.models import User
from .database.utils import get_all_user_todos_from_db


async def get_user_todos(user: User = Depends(get_current_user),
                         session: AsyncSession = Depends(get_async_session)):
    data = await get_all_user_todos_from_db(user.id, session)
    list_of_todos = []
    for item in data:
        list_of_todos.append(item[0])
    return list_of_todos
