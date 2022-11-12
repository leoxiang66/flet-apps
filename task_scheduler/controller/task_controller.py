from .base import BaseController
import flet as ft
import asyncio



class TaskController(BaseController):
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
    def submit(cls,e,page:ft.Page,task_widget,class_):
        task = task_widget.submit()
        card = class_(task,page)
        task_widget.reset()

        # page update
        cls.update_task_widget_in_page(page)
        page.homepage.insert_widget(card, 1,1)
        page.homepage.refresh()

        # async run
        asyncio.run(task.__await__())

    @classmethod
    def starr_task(cls, e,page,task, class_):
        #todo: check if already stored


        # 1. add a column 3
        page.homepage.append_widget(class_(task.name), 2)
        page.update()

        # 2. store locally
        # task.to_json(f'./.cache/{task.name}.json')








