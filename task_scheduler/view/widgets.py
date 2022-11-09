import flet as ft
from .base import BaseView


class BaseWidget(BaseView):
    def __init__(self, page: ft.Page) -> None:
        super().__init__(page)

    def add_widget(self, widget: ft.Control, widget_name: str, controllers: dict = None, add_to_page=False):
        super().add_widget(widget, widget_name, controllers, False)

    def to_flet(self):
        raise NotImplementedError()



class TaskWidget(BaseWidget):
    def __init__(self, page: ft.Page) -> None:
        super().__init__(page)
        self.add_widget(ft.Markdown('## Create a new task'),widget_name='title')
        self.add_widget(ft.TextField(label='Task Name', value='My Task'),widget_name='task_name_input')
        self.add_widget(ft.TextButton('Submit'),widget_name='submit_button',controllers=dict(
            on_click = None # todo
        ))
        self.add_widget(ft.TextButton('Add a todo'),widget_name='add_todo_button', controllers=dict(
            on_click = None # todo
        ))

    def to_flet(self):
        return ft.Column(controls=[
            self.get_widget('title'),
            self.get_widget('task_name_input'),
            ft.Row(
                controls=[
                    self.get_widget('submit_button'),
                    self.get_widget('add_todo_button')
                ]
            )
        ]
                                  )