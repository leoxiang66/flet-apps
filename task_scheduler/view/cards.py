import functools

import flet as ft
from ..model.base import BaseModel
from flet import colors
from ..model.tasks import Task
from ..utils import convert_time
from flet import icons
from ..controller import TaskController
import pygame.mixer as mixer
from pathlib import Path

SOUND_PATH = str(Path(__file__).absolute().parent.parent) + '/static/tishi.mp3'

class TaskCardPreview(ft.Card):
    def __init__(self,task_name:str, **kwargs):
        super(TaskCardPreview, self).__init__()

        self.width = 200
        self.task = kwargs.get('task', None)
        self.page = kwargs.get('page', None)


        self.content = ft.Column(
            controls=[
                ft.Markdown(f'## {task_name}'),
                ft.Row(controls=[
                    ft.IconButton(icon=icons.PLAY_ARROW, on_click=functools.partial(
                        TaskController.load_from_starred,page= self.page,task_name = task_name,
                        task_type = self.task.__class__,
                        taskcard_type = TaskCard
                    )),
                    ft.IconButton(icon=icons.REMOVE, on_click=functools.partial(
                        TaskController.delete_starred,
                        page = self.page,
                        task_name = task_name
                    ))
                ],alignment='center')
            ],
            horizontal_alignment='center'
        )






class TaskCard(BaseModel,ft.Card):
    def __init__(self,task: Task,page,width:int = 200, *args,**kwargs):
        BaseModel.__init__(self)
        ft.Card.__init__(self,*args,**kwargs)

        self.task = task
        self.width = width
        controls = [ft.Markdown(f'## {task.name}')]

        def callback(remain_time, **kwargs):
            checkbox = kwargs['checkbox']
            todo = kwargs['todo']

            checkbox.label = f'''{todo.todo_name}: {remain_time}s'''
            self.page.update()
            if remain_time == 0:
                checkbox.value = True

                mixer.init()
                mixer.music.load(SOUND_PATH)
                mixer.music.play()

                # TaskController.taskcard_expire(page, task.name) # todo

        for todo in task.getTodos():
            print(todo.todo_name)
            checkbox = ft.Checkbox(label= f'''{todo.todo_name}: {convert_time(todo.time)}s''', value=False, disabled=True,
                                   fill_color={"": colors.CYAN,},)
            controls.append(checkbox)
            todo.callback = functools.partial(callback,checkbox = checkbox, todo = todo)

        # starring
        controls.append(ft.IconButton(icon='favorite',on_click=functools.partial(TaskController.starr_task,page=page,task=task,class_=TaskCardPreview)))
        self.content = ft.Column(controls=controls,horizontal_alignment='center')


    def __hash__(self):
        return hash(self.content)





