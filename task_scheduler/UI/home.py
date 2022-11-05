import flet as ft
from flet import *
from .task_create_view import TaskView



def home(page: ft.Page):
    page.horizontal_alignment = 'center'
    page.add(ft.Markdown('# Task Scheduler'))
    page.title = 'Task Scheduler'
    page.scroll = 'adaptive'
    page.window_width = 900
    page.window_height = 500


    task_view = TaskView(page)

    col1 = task_view.getView()

    col2 = Container(content=Column(
        controls=[
        ft.Markdown('## Current Tasks')
    ],
        alignment="start",
        expand=True
    ),

        padding=10,
        alignment=ft.alignment.top_left
    )


    row1 = Row(
        controls=[
            col1,
            ft.VerticalDivider(width=12),
            col2
        ],
        vertical_alignment='start',
        expand=True,
        alignment= 'center'
    )
    page.body = row1
    page.add(row1)



if __name__ == '__main__':
    ft.app(target=home)