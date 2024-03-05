from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from auth.database.models import User
from sqlalchemy.ext.declarative import declarative_base
from uuid import UUID, uuid4


Base = declarative_base()


class ToDo(Base):
    __tablename__ = "todo"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=True)
    start_time: Mapped[datetime] = mapped_column(nullable=True)
    finish_time: Mapped[datetime] = mapped_column(nullable=True)
    is_finished: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey(User.id), nullable=False)

