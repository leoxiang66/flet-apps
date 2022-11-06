import flet as ft
from flet import *
from .task_create_view import TaskView
from ..task import starred_view_update as starred_view_update,read_tasks



def home(page: ft.Page):
    page.horizontal_alignment = 'center'
    page.add(ft.Markdown('# Task Scheduler'))
    page.title = 'Task Scheduler'
    page.scroll = 'adaptive'
    page.window_width = 1000
    page.window_height = 500


    task_view = TaskView(page)

    col1 = task_view.getView()

    col2 = Container(content=Column(
        controls=[
            ft.Markdown('## Current Tasks')
        ],
        alignment="start",
        expand=True,
    ),

        padding=10,
        alignment=ft.alignment.top_left
    )

    col3 = Container(content=Column(
        controls=[
            ft.Markdown('## Starred Tasks')
        ],
        alignment="start",
        horizontal_alignment='center'
    ),
        padding=10,
        alignment=ft.alignment.top_left
    )

    row1 = Row(
        controls=[
            col1,
            ft.VerticalDivider(width=12),
            col2,
            col3
        ],
        vertical_alignment='start',
        expand=True,
        alignment= 'center'
    )
    page.body = row1
    page.add(row1)
    starred_view_update(page,read_tasks(page))



if __name__ == '__main__':
    ft.app(target=home)