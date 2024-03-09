from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from fastui import prebuilt_html
from fastui.events import GoToEvent

from auth.router import router as auth_router
from todo.router import router as todo_router
from fastapi import status, HTTPException
from fastapi.responses import RedirectResponse
from fastui import components as c

app = FastAPI()

app.include_router(
    router=auth_router,
    tags=['Auth']
)
app.include_router(
    router=todo_router,
    tags=["ToDo"]
)


@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
async def validate_unauthorized(req, _):
    return RedirectResponse(url="/api/auth/", status_code=303)


@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='ToDo'))


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)