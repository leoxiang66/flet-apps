
from typing import List

import flet as ft
from .dialog import Dialogue
from ..task import Task,Todo,current_view_update



class TodoView:
    alert_dialogue = Dialogue('Please enter task time')

    def __init__(self, id, parent_controls: List, page:ft.Page, parent):
        print(id)
        self.id = id
        self.parent_controls = parent_controls
        self.page = page
        self.name = ft.TextField(label='Todo Name' ,value=f'''Todo {id-1}''', autofocus=True)
        self.time = ft.Dropdown(label='Todo_time', options=[
                        ft.dropdown.Option('30 Seconds'),
                        ft.dropdown.Option('1 Minute'),
                        ft.dropdown.Option('3 Minutes'),
                        ft.dropdown.Option('5 Minutes'),
                        ft.dropdown.Option('10 Minutes'),
                        ft.dropdown.Option('15 Minutes'),
                        ft.dropdown.Option('20 Minutes'),
                        ft.dropdown.Option('30 Minutes'),
                    ])
        self.parent = parent
        parent.todos.append(self)
        self.alert_dialogue.page = page

    def load_from_Todo(self,todo: Todo):
        self.name.value = todo.name
        self.time.value = todo.time
    def to_Todo(self) -> Todo:
        if self.time.value is None:
            self.alert_dialogue.open_dialog()
            raise ValueError('No value is given for time.')
        return Todo(self.name.value,self.time.value)

    def remove_todo(self,event):
        assert self.id>1
        self.parent_controls.pop(self.id)
        self.page.update()
        self.update_ids()

    def update_ids(self):
        for id in range(self.id-1,len(self.parent.todos)):
            todo = self.parent.todos[id]
            todo.id -= 1

        self.parent.todos.pop(self.id-2)



    def getValues(self):
        return dict(
            todo_name = self.name.value,
            time = self.time.value
        )

    def view(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Markdown('''### Todo'''),
                    self.name,
                    self.time,
                    ft.TextButton('Delete Todo',on_click=self.remove_todo )
                ]
        ),
            padding=10,
            border_radius=10,
            border=ft.border.all(1, ft.colors.BLACK26)

        )


class TaskView:
    alert_dialogue = Dialogue('Please enter task time')
    alert_dialogue2 = Dialogue('Please add Todos')
    def __init__(self, page:ft.Page):
        self.alert_dialogue.page = page
        self.alert_dialogue2.page = page
        self.page = page
        self.title = ft.Markdown('## Create a New Task')
        self.name = ft.TextField(label='Task Name', value='My Task')


        self.main_task = ft.Container(
            content=ft.Column(
                controls=[
                    self.name,
                ]
            )
        )

        self.buttons = ft.Row(
            controls=[
                ft.TextButton('Submit', on_click=self.getInfo),
                ft.TextButton('Add a todo', on_click=self.add_sub_task),
            ]
        )

        self.view = ft.Column(controls=[
            self.title,
            self.main_task,
            self.buttons
        ])

        self.todos  = []

    def getView(self):
        return ft.Container(
            content=self.view,
            width=400
        )

    def todo_view(self):
        index = len(self.view.controls)-1
        todo = TodoView(index, parent_controls=self.view.controls, page=self.page, parent=self)
        return todo.view()


    def add_sub_task(self,event):
        view = self.view
        controls = view.controls # list
        controls.insert(-1,self.todo_view())
        self.page.update()

    def getInfo(self,event):
        if len(self.todos) == 0:
            self.alert_dialogue2.open_dialog()
            return

        try:
            task = Task(self.name.value, list(map(lambda x: x.to_Todo(), self.todos)), self.page)
        except:

            return

        ## page
        current_view_update(self.page,task,False, self )






    def getValues(self):
        return dict(
            task_name=self.name.value,

        )





