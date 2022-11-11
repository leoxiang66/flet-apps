import flet
from flet import Column, ElevatedButton, Text, TextField

def main(page):

    first_name = TextField(label="First name", autofocus=True)
    last_name = TextField(label="Last name")
    greetings = Column()

    def btn_click(e):
        greetings.controls.append(Text(f"Hello, {first_name.value} {last_name.value}!"))
        first_name.value = ""
        last_name.value = ""
        page.update()
        first_name.focus()

    page.add(
        first_name,
        last_name,
        ElevatedButton("Say hello!", on_click=btn_click),
        greetings,
    )

if __name__ == '__main__':
    flet.app(target=main)