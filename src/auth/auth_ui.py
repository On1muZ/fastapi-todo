from fastapi import APIRouter
from fastui import components as c, FastUI
from auth.schemas import CreateUser
from auth.router import router


@router.get('/sign_up', response_model=FastUI, response_model_exclude_none=True)
async def get_sign_up_page():
    return [
        c.PageTitle(text="Sign Up"),
        c.Page(
            components=[
                c.Heading(text="Welcome New User!", level=2),
                c.Paragraph(text="Please enter your username and password to use this site"),
                c.ModelForm(
                    model=CreateUser,
                    submit_url="/api/sign_up"
                )
            ]
        )
    ]
