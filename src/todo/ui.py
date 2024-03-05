from uuid import UUID
from fastui.events import GoToEvent, PageEvent, BackEvent
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import ToDo as BaseToDo
from database import get_async_session
from .database.models import ToDo
from .database.utils import get_todo_by_id
from .dependencies import get_user_todos
from auth.database.models import User
from auth.dependencies import get_current_user
from .router import router
from fastui import components as c, FastUI
from .schemas import CreateToDo


@router.get("/", response_model=FastUI, response_model_exclude_none=True)
async def main_page(user: User = Depends(get_current_user),
                    todos: list[ToDo] = Depends(get_user_todos)):
    components = [
        c.Heading(text="ToDo", level=1),
        c.Heading(text=f'Welcome back {user.username}!', level=2),
        c.Button(text='Create ToDo', on_click=GoToEvent(url='/todo/create/'),
                 class_name='btn btn-outline-success btn-lg border border-3 rounded rounded-5'),
        c.Paragraph(text=' '),
        c.Button(text='Finished ToDos', on_click=GoToEvent(url='/todo/finished/'),
                 class_name='btn btn-outline-info btn-lg border border-3 rounded rounded-5'),
    ]
    for i in todos:
        components.append(c.Paragraph(text=''))
        if not i.is_finished:
            components.append(
                c.Div(
                    components=[
                        c.Heading(text=i.name, level=3),
                        c.Paragraph(text=i.text if i.text is not None else ""),
                        c.Heading(text=f"Start time: {i.start_time}" if i.start_time is not None else "", level=6),
                        c.Heading(text=f"Finish time: {i.finish_time}" if i.finish_time is not None else "", level=6),
                        c.Button(text="View ToDo", on_click=GoToEvent(url=f"/todo/view/{i.id}"),
                                 class_name="btn btn-outline-info btn-lg border border-3 rounded rounded-5"),
                    ],
                    class_name="p-3 mb-2 bg-success text-white rounded text-center"
                               " rounded-5 border border-5"
                )
            )
    return [
        c.PageTitle(text="ToDo"),
        c.Page(
            components=components,
        )
    ]


@router.get("/create/", response_model=FastUI, response_model_exclude_none=True)
async def create_todo_page(user: User = Depends(get_current_user)):
    return [
        c.PageTitle(text='Create ToDo'),
        c.Page(
            components=[
                c.Heading(text="ToDo", level=1),
                c.Heading(text=f"Create Your ToDo, {user.username}", level=2),
                c.ModelForm(
                    model=CreateToDo,
                    method="POST",
                    display_mode='page',
                    submit_url="/api/todo/create",
                )
            ]
        )
    ]


@router.get('/view/{todo_id}', response_model=FastUI, response_model_exclude_none=True)
async def view_todo_page(todo_id: UUID,
                         session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(get_current_user)):
    todo = await get_todo_by_id(todo_id, session)
    if user.id != todo.user_id:
        return [c.FireEvent(event=GoToEvent(url='/todo/'))]
    return [
        c.PageTitle(text="ToDo"),
        c.Page(
            components=[
                c.Heading(text="ToDo", level=1),
                c.ModelForm(
                    model=BaseToDo,
                    initial=BaseToDo(
                        name=todo.name,
                        text=todo.text,
                        time_to_start=todo.start_time,
                        time_to_finish=todo.finish_time,
                        completed=todo.is_finished,
                    ).dict(),
                    footer=[],
                    submit_url=f"/api/todo/update/{todo.id}/",
                    submit_trigger=PageEvent(name='update-todo')
                ),
                c.Button(text='Update',
                         class_name="btn btn-outline-success btn-lg border border-3 rounded rounded-5",
                         on_click=PageEvent(name='update-todo')),
                c.Paragraph(text=''),
                c.Form(
                    submit_url=f"/api/todo/delete/{todo.id}",
                    submit_trigger=PageEvent(name='delete-todo'),
                    footer=[],
                    form_fields=[]
                ),
                c.Button(text='Delete',
                         class_name="btn btn-outline-danger btn-lg border border-3 rounded rounded-5",
                         on_click=PageEvent(name='delete-todo')),
                c.Paragraph(text=''),
                c.Button(text="Back",
                         class_name='btn btn-outline-info btn-lg border border-3 rounded rounded-5',
                         on_click=BackEvent())
            ]
        )
    ]


@router.get('/finished/', response_model=FastUI, response_model_exclude_none=True)
async def finished_todo_page(todos: list[ToDo] = Depends(get_user_todos),
                             user: User = Depends(get_current_user)):
    components = [
        c.Heading(text="Finished ToDo", level=1),
        c.Heading(text=f'Welcome back {user.username}!', level=2),
        c.Button(text='Back', on_click=BackEvent(),
                 class_name='btn btn-outline-info btn-lg border border-3 rounded rounded-5'),
    ]
    for i in todos:
        components.append(c.Paragraph(text=''))
        if i.is_finished:
            components.append(
                c.Div(
                    components=[
                        c.Heading(text=i.name, level=3),
                        c.Paragraph(text=i.text if i.text is not None else ""),
                        c.Heading(text=f"Start time: {i.start_time}" if i.start_time is not None else "", level=6),
                        c.Heading(text=f"Finish time: {i.finish_time}" if i.finish_time is not None else "", level=6),
                        c.Button(text="View ToDo", on_click=GoToEvent(url=f"/todo/view/{i.id}"),
                                 class_name="btn btn-outline-info btn-lg border border-3 rounded rounded-5"),
                    ],
                    class_name="p-3 mb-2 bg-warning text-white rounded text-center"
                               " rounded-5 border border-5"
                )
            )
    return [
        c.PageTitle(text="ToDo"),
        c.Page(
            components=components,
        )
    ]
