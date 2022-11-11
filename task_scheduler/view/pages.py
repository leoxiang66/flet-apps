import flet as ft
from .base import MultiRowsView,MultiColumnsView
from typing import List, Union

class HomePage():
    def __init__(self, page: ft.Page,num_containers: int,container_names: List[str] = None,pattern:str = 'multi-column' ) -> None:
        super().__init__()
        self.pattern = pattern
        if pattern == 'multi-column':
            self.view = MultiColumnsView(page,num_containers,container_names)
        elif pattern == 'multi-row':
            self.view = MultiRowsView(page, num_containers, container_names)

        else:
            raise NotImplementedError()

    def get_container(self, container: Union[int,str]):
        if isinstance(container,str):
            return self.view.get_widget(container)
        else:
            widget_name = f'{self.pattern[6:]}_{container}'
            return self.view.get_widget(widget_name)

    def add_widget(self,widget: ft.Control, container: Union[int,str]):
        self.get_container(container).controls.append(widget)

    def refresh(self):
        self.view.page.update()


