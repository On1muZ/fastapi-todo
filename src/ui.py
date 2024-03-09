from fastui import components as c, AnyComponent


def demo_page(*components: AnyComponent, title: str = 'ToDo') -> list[AnyComponent]:
    from fastui.events import GoToEvent
    return [
        c.PageTitle(text=title),
        c.Navbar(
            title=title,
            title_event=GoToEvent(url='/todo/'),
            start_links=[
                c.Link(
                    components=[c.Text(text='Auth')],
                    on_click=GoToEvent(url='/auth/'),
                    active='startswith:/auth/'
                ),
                c.Link(
                    components=[c.Text(text='ToDos')],
                    on_click=GoToEvent(url='/todo/'),
                    active='startswith:/todo/'
                ),
                c.Link(
                    components=[c.Text(text='Finished ToDos')],
                    on_click=GoToEvent(url='/todo/finished/'),
                    active='startswith:/todo/finished/'
                ),
            ]
        ),
        c.Page(
            components=[
                c.Heading(text=title, level=1),
                *components
            ]
        ),
        c.Footer(
            extra_text=title,
            links=[
                c.Link(
                    components=[c.Text(text='Github')], on_click=GoToEvent(url='https://github.com/On1muZ')
                ),
            ],
        ),
    ]
