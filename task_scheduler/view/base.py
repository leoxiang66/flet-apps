import flet as ft
from typing import List, Union
from ..model.base import BaseModel



class BaseView(BaseModel):
    def __init__(self,page: ft.Page) -> None:
        super().__init__()
        self.page = page
        self.widgets = {}

    def add_widget(self, widget: ft.Control, widget_name: str, controllers: dict = None, add_to_page = True):
        self.widgets[widget_name] = (widget, controllers)
        if add_to_page:
            self.page.controls.append(widget)


    def refresh_page(self):
        self.page.update()

    def get_widget(self, widget_name: str) -> Union[ft.Control, None]:
        ret = self.widgets.get(widget_name, None)
        return ret[0] if ret is not None else ret

    def __str__(self):
        ret= 'widgets:\n'
        for i,j in self.widgets.items():
            ret += i + str(j) + '\n'
        return ret

class MultiColumnsView(BaseView):
    def __init__(self, page: ft.Page, num_columns: int, column_names: List[str] = None) -> None:
        super().__init__(page)
        controls = [ft.Container(content=ft.Column(
            alignment="start",
            expand=True,
            ),
            padding= 10,
            alignment=ft.alignment.top_left
        ) for _ in range(num_columns)]

        self.add_widget(ft.Row(controls=controls,
                               vertical_alignment='start',
                               expand=True,
                               alignment='center',
                               spacing=100
                               ), widget_name='__row__')

        if column_names is None:
            for i in range(num_columns):
                self.add_widget(controls[i].content,f'column_{i}',add_to_page=False)

        else:
            assert num_columns == len(column_names)
            for i in range(num_columns):
                self.add_widget(controls[i].content,column_names[i],add_to_page=False)

class MultiRowsView(BaseView):
    def __init__(self, page: ft.Page, num_rows: int, row_names: List[str] = None) -> None:
        super().__init__(page)

        controls = [ft.Container(content=ft.Row(
            alignment="start",
            expand=True,
        ),
            padding=10,
            alignment=ft.alignment.top_left
        ) for _ in range(num_rows)]

        self.add_widget(ft.Column(controls=controls,
                               horizontal_alignment='start',
                               expand=True,
                               alignment='center',
                                spacing=100
                               ), widget_name='__column__')

        if row_names is None:
            for i in range(num_rows):
                self.add_widget(controls[i].content, f'row_{i}', add_to_page=False)

        else:
            assert num_rows == len(row_names)
            for i in range(num_rows):
                self.add_widget(controls[i].content, row_names[i], add_to_page=False)





