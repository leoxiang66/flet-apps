import functools

import flet as ft
from ..model.base import BaseModel
from flet import colors
from ..model.tasks import Task
from ..utils import convert_time
from flet import icons
from ..controller import TaskController

class TaskCardPreview(ft.Card):
    def __init__(self,task_name:str ,*args, **kwargs):
        super(TaskCardPreview, self).__init__(*args,**kwargs)

        self.width = 200
        self.content = ft.Column(
            controls=[
                ft.Markdown(f'## {task_name}'),
                ft.Row(controls=[
                    ft.IconButton(icon=icons.PLAY_ARROW), # todo
                    ft.IconButton(icon=icons.REMOVE) # todo
                ],alignment='center')
            ],
            horizontal_alignment='center'
        )



class TaskCard(BaseModel,ft.Card):
    def __init__(self,task: Task,page,width:int = 200, *args,**kwargs):
        BaseModel.__init__(self)
        ft.Card.__init__(self,*args,**kwargs)

        self.width = width
        controls = [ft.Markdown(f'## {task.name}')]
        for todo in task.getTodos():
            checkbox = ft.Checkbox(label= f'''{todo.todo_name}: {convert_time(todo.time)}s''', value=False, disabled=True,
                                   fill_color={"": colors.CYAN,},)
            controls.append(checkbox)


            def callback(remain_time):
                checkbox.label = f'''{todo.todo_name}: {remain_time}s'''
                if remain_time == 0:
                    checkbox.value = True
                    #todo playsound
                self.page.update()
            todo.callback = callback

        # starring
        controls.append(ft.IconButton(icon='favorite',on_click=functools.partial(TaskController.starr_task,page=page,task=task,class_=TaskCardPreview)))
        self.content = ft.Column(controls=controls,horizontal_alignment='center')


    def __hash__(self):
        return hash(self.content)





