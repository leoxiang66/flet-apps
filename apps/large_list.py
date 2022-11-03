import flet
from flet import Page, Text,ListView

def main(page: Page):
    for i in range(100):
        page.controls.append(Text(f"Line {i}"))
    page.scroll = "always"
    page.update()



def main2(page: Page):
    lv = ListView(expand=True, spacing=10)
    for i in range(100):
        lv.controls.append(Text(f"Line {i}"))
    page.add(lv)

flet.app(target=main)

if __name__ == '__main__':
    # flet.app(target=main)
    flet.app(target=main2)