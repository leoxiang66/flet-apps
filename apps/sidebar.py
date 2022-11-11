import flet as ft
from flet import (
    Column,
    Container,
    Page,
    Row,
    colors,
)



def main(page: Page):

    # page.window_height =560
    # page.window_width = 750
    page.window_resizable = False

    col1 = Container(content=Column(controls=
                                    [
                                        ft.Markdown('''# Literature Research Tool'''),
                                        ft.Markdown('''**Choose the platforms**'''),
                                        ft.Checkbox(label="IEEE", value=False)
                                    ]),
                width=300,
                height=page.window_height - 20,
                padding=5,
                # bgcolor=colors.CYAN_100
                
            )  
    col2 = Container(content=Column(controls=[
        ft.Text('tets')
    ],
                alignment="start",
                expand=True
                ),
                # width=700,
                # height=page.window_height - 20,
                padding=5,
                # bgcolor=colors.GREEN
                
            )   
    
    row1 =Row(
            controls=[
            col1,
            ft.VerticalDivider(width=1,opacity=0.2),
            col2
        ],
        expand=True,
    )
    
    
    page.add(row1)


if __name__ == '__main__':
    ft.app(target=main)