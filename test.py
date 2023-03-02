import flet as ft

md1 = """
# Markdown Example
Markdown allows you to easily include formatted text, images, and even formatted Dart code in your app.

## Titles

Setext-style

This is an H1
=============

This is an H2
-------------

Atx-style

# This is an H1

## This is an H2

###### This is an H6

Select the valid headers:

- [x] `# hello`
- [ ] `#hello`


"""

def main(page: ft.Page):
    # page.horizontal_alignment='stretch'

    container = ft.Container(content=ft.Text(
            md1,
            selectable=True,
    ),
        width=20)

    page.scroll = "auto"
    page.add(
        container
        )
    page.update()

ft.app(target=main)