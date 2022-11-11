import flet as ft
import time

def main(page: ft.Page):
    # add/update controls on Page
    t = ft.Text()
    page.add(t)  # it's a shortcut for page.controls.append(t) and then page.update()

    for i in range(2):
        t.value = f"Step {i}"
        page.update()
        time.sleep(1)

    page.add(
        ft.Row(controls=[
            ft.Text("A"),
            ft.Text("B"),
            ft.Text("C")
        ])
    )
    page.add(
        ft.Row(controls=[
            ft.Text("A"),
            ft.Text("B"),
            ft.Text("C")
        ])
    )
    name = ft.TextField(label="Your name")

    def say_hello(event):
        page.add(ft.Markdown(f'**Hi {name.value}**'))



    page.add(
        ft.Row(controls=[
            name,
            ft.ElevatedButton(text="Say my name!",on_click=say_hello)
        ])
    )

if __name__ == '__main__':
    # flet.app(target=main,view=flet.WEB_BROWSER)
    ft.app(target=main)