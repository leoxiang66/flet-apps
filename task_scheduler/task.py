import functools
import flet as ft
from .UI.task_card_view import TaskCard
from .io.base import IO
from flet import icons
from .utils import CACHE_PATH
import os
from os import listdir

def read_starred():
    cache_path = './.cache/'
    if os.path.isdir(cache_path):
        jsonfiles = set([f for f in listdir(cache_path) if f.endswith('.json')])
        return jsonfiles

class Todo:
    def __init__(self, todo_name:str, time: str):

        self.name = todo_name
        self.time = time

    def getValues(self):

        return dict(
            todo_name = self.name,
            time = self.time
        )

    @classmethod
    def load_from_dict(cls,dict_obj:dict):
        return cls(dict_obj['todo_name'], dict_obj['time'])



class Task(IO):
    STARRED = read_starred()
    def __init__(self, title: str, todos: list, page):
        self.title = ft.Markdown(f'### {title}')
        self.todos = todos
        self.subtask_cards = []
        self.page = page
        for todo in self.todos:
            info = todo.getValues()
            task_name = info['todo_name']
            time = info['time']
            todo_card = TaskCard(task_name,time,page)
            self.subtask_cards.append(todo_card)

    def to_view(self, only_title = False, store_icon = True) -> TaskCard:
        if only_title:
            return TaskCard('','',content=self.title,page=self.page)
        else:

            controls = [self.title] + self.subtask_cards
            if store_icon:
                controls.append(ft.IconButton(icon=icons.FAVORITE, on_click=self.to_json_event))

            return TaskCard('', '',
                     content=ft.Column(controls=controls, horizontal_alignment='center'),
                     page=self.page
                     )

    def toDict(self) -> dict:
        todo_dict = [] # [dic t]
        for i in self.todos:
            todo_dict.append(i.getValues())
        return dict(
            title = self.title.value[4:],
            todos = todo_dict
        )

    def to_json_event(self,event):
        title = self.title.value[4:] +'.json'
        if title not in self.STARRED:
            self.to_json()
            starred_view_update(self.page, self)
            self.STARRED.add(title)
        else:
            print('already starred')

    def to_json(self, file_path:str = None):
        if file_path is None:
            file_path = CACHE_PATH() +f'''{self.title.value[4:]}.json'''
        self.dict_to_json(self.toDict(),file_path)

    @classmethod
    def load_from_json(cls, file_path:str,page):
        dict_obj =  cls.json_to_dict(file_path)
        todos = []
        for i in dict_obj['todos']:
            todos.append(Todo.load_from_dict(i))
        return cls(dict_obj['title'], todos,page)




def current_view_update(page,task, update:bool = True, task_view = None, **kwargs):
    page.body.controls[2].content.controls.insert(1,task.to_view(**kwargs))
    if update:
        page.update()

    if task_view is not None:
        while len(task_view.view.controls) > 3:
            task_view.view.controls.pop(2)
        task_view.todos.clear()
        task_view.page.update()


    ## thread issues
    for thr in task.subtask_cards:
        thr.start()
        thr.join()



def delete_favorite_and_update_view(env,page,file_name:str,starred_set):
    cache_path = './.cache/'
    path = cache_path + file_name

    if os.path.exists(path):
        os.remove(path)
        col3 = page.body.controls[3]
        col3.content.controls = col3.content.controls[:1]
        starred_view_update(page,read_tasks(page))
        starred_set.remove(file_name)




def starred_view_update(page, tasks):
    if tasks is None:
        return
    if not isinstance(tasks,list):
        tasks = [tasks]
    col3 = page.body.controls[3]


    for task in tasks:
        col3.content.controls.append(
            ft.Card(content=ft.Row(controls=[
            task.title,
            ft.IconButton(icon=icons.PLAY_ARROW,on_click=functools.partial(current_view_update,page,task,store_icon=False)),
            ft.IconButton(icon=icons.REMOVE,on_click=functools.partial(delete_favorite_and_update_view,page=page,file_name=f'{task.title.value[4:]}.json',starred_set=task.STARRED))
        ])))
    page.update()




def read_tasks(page):
    cache_path = './.cache/'
    if os.path.isdir(cache_path):
        ret = []
        jsonfiles = set([f for f in listdir(cache_path) if f.endswith('.json')])
        for jsonfile in jsonfiles:
            ret.append(Task.load_from_json(cache_path+jsonfile,page))
        return ret