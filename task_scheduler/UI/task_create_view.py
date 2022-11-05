from typing import List
from .task_card_view import TaskCard
import flet as ft
from .dialog import Dialogue
from flet import colors



class Todo:
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
                        ft.dropdown.Option('30 Minutes'),
                    ])
        self.parent = parent
        parent.todos.append(self)
        self.alert_dialogue.page = page

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
        if self.time.value is None:
            self.alert_dialogue.open_dialog()
            return


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
            border=ft.border.all(1, colors.BLACK26)

        )

class TaskView:
    alert_dialogue = Dialogue('Please enter task time')
    def __init__(self, page:ft.Page):
        self.alert_dialogue.page = page
        self.page = page
        self.title = ft.Markdown('## Create a New Task')
        self.name = ft.TextField(label='Todo Name', value='My Task')


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
        todo = Todo(index, parent_controls=self.view.controls, page=self.page, parent=self)
        return todo.view()


    def add_sub_task(self,event):
        view = self.view
        controls = view.controls # list
        controls.insert(-1,self.todo_view())
        self.page.update()

    def getInfo(self,event):

        sub_cards = [ft.Markdown(f'### {self.name.value}')]
        time = ''
        for todo in self.todos:
            info = todo.getValues()
            task_name = info['todo_name']
            time = info['time']
            todo_card = TaskCard(task_name,time,self.page)
            sub_cards.append(todo_card)



        task_card = TaskCard(self.name.value,time,
                             content= ft.Column(controls=sub_cards,horizontal_alignment='center'),
                             page= self.page
                             )

        ## page
        self.page.body.controls[2].content.controls.append(task_card)
        while len(self.view.controls) > 3:
            self.view.controls.pop(2)
        self.page.update()
        self.todos.clear()

        ## thread issues
        for i in range(1,len(sub_cards)):
            thr = sub_cards[i]
            thr.start()
            thr.join()


    def getValues(self):
        return dict(
            task_name=self.name.value,

        )





