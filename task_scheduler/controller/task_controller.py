from .base import BaseController
import flet as ft
import asyncio
import os
from os import listdir
from os.path import join



class TaskController(BaseController):
    CACHE_PATH = './.cache/'
    if not os.path.isdir(CACHE_PATH):
        os.mkdir(CACHE_PATH)

    @classmethod
    def update_task_widget_in_page(cls,page):
        page.homepage.remove_widget(0, -1)
        page.homepage.append_widget(page.homepage.task_widget.to_flet(), 0)
        page.homepage.refresh()

    @classmethod
    def add_a_todo(cls,e,page: ft.Page,task_widget):
        task_widget.add_todo(len(task_widget.todo_widgets))
        cls.update_task_widget_in_page(page)


    @classmethod
    def delete_a_todo(cls,e,page: ft.Page,todo):
        page.homepage.task_widget.delete_todo(todo.id)
        cls.update_task_widget_in_page(page)


    @classmethod
    def submit(cls, e, page:ft.Page, task_widget, taskcard_type):
        task = task_widget.submit()
        card = taskcard_type(task, page)
        task_widget.reset()

        # page update
        cls.update_task_widget_in_page(page)
        page.homepage.insert_widget(card, 1,1)
        page.homepage.refresh()

        # async run
        asyncio.run(task.__await__())


    @classmethod
    def taskcard_expire(cls, page, task_name):
        cards = page.homepage.get_container(1).controls
        # id = -1
        for i in range(1, len(cards)):
            card = cards[i]
            if card.task.name == task_name:
                card.opacity = 0.9
                card.content.controls[0].value = f'{card.task.name} (DONE)'
                page.homepage.refresh()
                break

        # if id != -1:
        #     page.homepage.remove_widget(1, id)
        #     page.homepage.refresh()


    @classmethod
    def starr_task(cls, e,page,task, class_):
        if not os.path.isdir(cls.CACHE_PATH):
            os.mkdir(cls.CACHE_PATH)

        # if not os.path.exists(cls.CACHE_PATH+f'{task.name}.json'):
        # 1. add a column 3
        page.homepage.append_widget(class_(task.name,task=task,page=page), 2)
        page.update()

        # 2. store locally
        task.to_json(f'{cls.CACHE_PATH}{task.name}.json')

    @classmethod
    def load_from_starred(cls,e,page,task_name, task_type,taskcard_type ):
        path = cls.CACHE_PATH + task_name + '.json'
        task = task_type.from_json(path)

        card = taskcard_type(task, page)

        # page update
        page.homepage.insert_widget(card, 1, 1)
        page.homepage.refresh()

        # async run
        asyncio.run(task.__await__())

    @classmethod
    def delete_starred(cls,e,page,task_name):
        previews = page.homepage.get_container(2).controls
        id = -1
        for i in range(1,len(previews)):
            pre = previews[i]
            if pre.task.name == task_name:
                id = i
                break

        if id != -1:
            page.homepage.remove_widget(2,id)
            page.homepage.refresh()
            if os.path.exists(f'{cls.CACHE_PATH}{task_name}.json'):
                os.remove(f'{cls.CACHE_PATH}{task_name}.json')


    @classmethod
    def on_startup(cls,page, task_type, taskpreview_type):
        if not os.path.isdir(cls.CACHE_PATH):
            os.mkdir(cls.CACHE_PATH)
        files = [f for f in listdir(cls.CACHE_PATH) if f.endswith('.json')]
        for file in files:
            task= task_type.from_json(join(cls.CACHE_PATH,file))
            page.homepage.append_widget(taskpreview_type(task.name, task=task, page=page), 2)

        page.update()











