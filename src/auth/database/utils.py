from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User
from ..utils import get_password_hash
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status


async def save_user(username: str, password: str, session: AsyncSession):
    stmt = insert(User).values(
        username=username,
        hashed_password=get_password_hash(password)
    )
    try:
        await session.execute(stmt)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username has already take. Please try another one"
        )
    else:
        await session.commit()


async def get_user_by_username(username: str, session: AsyncSession) -> User:
    query = select(User).where(User.username == username)
    data = await session.execute(query)
    try:
       user = data.fetchone()[0]
    except TypeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect data")
    else:
        return user
