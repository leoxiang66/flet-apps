import flet as ft

class Dialogue:
    def __init__(self, msg: str, page: ft.Page= None):
        self.dialog = ft.AlertDialog(title=ft.Text(msg))
        self.page = page

    def open_dialog(self):
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()


def main(page: ft.Page):
    a = Dialogue('hi',page)
    a.open_dialog()

if __name__ == '__main__':
    ft.app(target=main)