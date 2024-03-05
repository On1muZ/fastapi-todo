from fastui import components as c, FastUI
from auth.schemas import CreateUser, LoginUser
from auth.router import router
from fastui.events import GoToEvent, BackEvent
from fastapi import Request
from fastapi.responses import RedirectResponse


@router.get('/sign_up', response_model=FastUI, response_model_exclude_none=True)
async def get_sign_up_page():
    return [
        c.PageTitle(text="Sign Up"),
        c.Page(
            components=[
                c.Div(
                    components=[
                        c.Heading(text="ToDo", level=1),
                        c.Heading(text="Welcome New User!", level=2),
                        c.Paragraph(text="Please enter your username and password to use this site"),
                        c.ModelForm(
                            model=CreateUser,
                            submit_url="/api/auth/sign_up",
                            method="POST",
                        ),
                        c.Paragraph(text='If you click to submit button,'
                                         ' you will agree with our conditions of usage'),
                        c.Button(text="Back", on_click=BackEvent())
                    ],
                ),
            ],
        )
    ]


@router.get("", response_model=FastUI, response_model_exclude_none=True)
async def auth_page():
    return [
        c.PageTitle(text='Auth'),
        c.Page(
            components=[
                c.Heading(text="ToDo", level=1),
                c.Heading(text="Sign in or Sign up", level=2),
                c.Button(text="Sign Up", on_click=GoToEvent(url="/auth/sign_up")),
                c.Paragraph(text="Click to sign up"),
                c.Button(text="Sign In", on_click=GoToEvent(url="/auth/sign_in")),
                c.Paragraph(text="Click to sign in"),
            ]
        )
    ]


@router.get("/sign_in", response_model=FastUI, response_model_exclude_none=True)
async def sign_in_page(request: Request):
    return [
        c.PageTitle(text='Sign In'),
        c.Page(
            components=[
                c.Heading(text="ToDo", level=1),
                c.Heading(text='Welcome back', level=2),
                c.ModelForm(
                    model=LoginUser,
                    submit_url="/api/auth/sign_in",
                    method="POST"
                ),
                c.Paragraph(text=''),
                c.Button(text="Back", on_click=BackEvent())
            ]
        )
    ]
