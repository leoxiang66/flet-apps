import flet as ft
from flet import colors
from .base import BaseView
from ..controller import TaskController
from ..model.tasks import Task
from typing import Type
from .cards import TaskCard

class BaseWidget(BaseView):
    def __init__(self, page: ft.Page) -> None:
        super().__init__(page)

    def add_widget(self, widget: ft.Control, widget_name: str, controllers: dict = None, add_to_page=False):
        super().add_widget(widget, widget_name, controllers, False)

    def to_flet(self):
        raise NotImplementedError()


class TodoWidget(BaseWidget):
    def __init__(self, page: ft.Page, id: int) -> None:
        super().__init__(page)
        self.id = id
        self.add_widget(ft.TextField(label='Todo Name', value=f'''Todo {id}''', autofocus=True)
                        , widget_name='todo_name_input')

        self.add_widget(ft.Dropdown(label='Todo Time', options=[
            ft.dropdown.Option('30 Seconds'),
            ft.dropdown.Option('1 Minute'),
            ft.dropdown.Option('3 Minutes'),
            ft.dropdown.Option('5 Minutes'),
            ft.dropdown.Option('10 Minutes'),
            ft.dropdown.Option('15 Minutes'),
            ft.dropdown.Option('20 Minutes'),
            ft.dropdown.Option('30 Minutes'),
        ]), widget_name='time_options')

        self.add_widget(ft.TextButton('Delete Todo'), widget_name='delete_todo_button',
                        controllers=TaskController.bind_controller('delete_todo_button',
                                                                   keywords=['on_click'],
                                                                   functions=[TaskController.delete_a_todo],
                                                                   args=[(page,self)])
                        )

    def to_flet(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    self.get_widget('todo_name_input'),
                    self.get_widget('time_options'),
                    self.get_widget('delete_todo_button')
                ]
            ),
            width= 280,
            padding=10,
            border_radius=10,
            border=ft.border.all(1, ft.colors.BLACK26)
        )

class TaskWidget(BaseWidget):
    def __init__(self, page: ft.Page) -> None:
        super().__init__(page)
        self.add_widget(ft.Markdown('## Create a new task'),widget_name='title')
        self.add_widget(ft.TextField(label='Task Name', value='My Task'),widget_name='task_name_input')
        self.add_widget(ft.TextButton('Submit'),widget_name='submit_button',controllers= TaskController.bind_controller(
            widget_name='submit_button',
            keywords=['on_click'],
            functions=[TaskController.submit],
            args=[(page,self,TaskCard)]
        )
                        ) # todo
        self.add_widget(ft.TextButton('Add a todo'),widget_name='add_todo_button', controllers=
                        TaskController.bind_controller('add_todo_button', ['on_click'],[TaskController.add_a_todo],[(page,self)])
                        )
        self.todo_widgets = []

    def to_flet(self):
        return ft.Column(controls=[
            self.get_widget('title'),
            self.get_widget('task_name_input'),
            ft.Column(controls=[x.to_flet() for x in self.todo_widgets]),
            ft.Row(
                controls=[
                    self.get_widget('submit_button'),
                    self.get_widget('add_todo_button')
                ]
            )
        ]
                                  )

    def reset(self):
        self.get_widget('task_name_input').value = 'My Task'
        self.todo_widgets.clear()

    def add_todo(self, id: int):
        self.todo_widgets.append(TodoWidget(self.page,id))

    def delete_todo(self,id: int):
        for i in range(id+1,len(self.todo_widgets)):
            todo_w = self.todo_widgets[i]
            todo_w.id -=1

        self.todo_widgets.pop(id)

    def submit(self):
        task = Task(self.get_widget('task_name_input').value)
        for todo in self.todo_widgets:
            task.add_todo(todo.get_widget('todo_name_input').value,time=todo.get_widget('time_options').value)

        return task



