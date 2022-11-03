import flet as ft
from flet import Page

def main(page: Page):
    # add/update controls on Page
    t = ft.Text(value="Hello, world!", color="green")
    page.controls.append(t)
    page.update()

if __name__ == '__main__':
    # flet.app(target=main,view=flet.WEB_BROWSER)
    ft.app(target=main)