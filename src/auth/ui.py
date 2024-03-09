from fastui import components as c, FastUI

from auth.database.models import User
from auth.dependencies import get_current_user
from auth.schemas import CreateUser, LoginUser
from auth.router import router
from fastui.events import GoToEvent, BackEvent, PageEvent
from fastapi import Request, Depends
from ui import demo_page


@router.get('/sign_up', response_model=FastUI, response_model_exclude_none=True)
async def get_sign_up_page():
    return demo_page(
        c.Div(
            components=[
                c.Heading(text="Welcome New User!", level=2),
                c.Paragraph(text="Please enter your username and password to use this site"),
                c.ModelForm(
                    model=CreateUser,
                    submit_url="/api/auth/sign_up",
                    method="POST",
                    footer=[],
                    submit_trigger=PageEvent(name='sign-up')
                ),
                c.Button(text="Sign Up", on_click=PageEvent(name="sign-up"),
                         class_name='btn btn-outline-success btn-lg border border-3 rounded rounded-5'),
                c.Paragraph(text='If you click to submit button,'
                                 ' you will agree with our conditions of usage'),
                c.Button(text="Back", on_click=BackEvent(),
                         class_name='btn btn-outline-info btn-lg border border-3 rounded rounded-5')
            ],
        )
    )


@router.get("/", response_model=FastUI, response_model_exclude_none=True)
async def auth_page(user: User | None = Depends(get_current_user)):
    if user is None:
        return demo_page(
            c.Heading(text='Auth Page', level=2),
            c.Heading(text="Sign in or Sign up", level=3),
            c.Button(text="Sign Up", on_click=GoToEvent(url="/auth/sign_up"),
                     class_name='btn btn-outline-info btn-lg border border-3 rounded rounded-5'),
            c.Paragraph(text="Click to sign up"),
            c.Button(text="Sign In", on_click=GoToEvent(url="/auth/sign_in"),
                     class_name='btn btn-outline-info btn-lg border border-3 rounded rounded-5'),
            c.Paragraph(text="Click to sign in"),
        )
    return demo_page(
        c.Heading(text='Auth Page', level=2),
        c.Heading(text='You are login as ' + user.username),
        c.Form(
            footer=[],
            submit_url="/api/auth/logout",
            submit_trigger=PageEvent(name='logout'),
            form_fields=[]
        ),
        c.Button(text='Logout', on_click=PageEvent(name='logout'),
                 class_name='btn btn-outline-danger btn-lg border border-3 rounded rounded-5'),
    )


@router.get("/sign_in", response_model=FastUI, response_model_exclude_none=True)
async def sign_in_page(request: Request):
    return demo_page(
                c.Heading(text='Welcome back', level=2),
                c.ModelForm(
                    model=LoginUser,
                    submit_url="/api/auth/sign_in",
                    method="POST",
                    footer=[],
                    submit_trigger=PageEvent(name='sign-in')
                ),
                c.Button(text="Sign In", on_click=PageEvent(name="sign-in"),
                         class_name='btn btn-outline-success btn-lg border border-3 rounded rounded-5'),
                c.Paragraph(text=''),
                c.Button(text="Back", on_click=BackEvent(),
                         class_name='btn btn-outline-info btn-lg border border-3 rounded rounded-5')
                     )
