import flet
from flet import (Container, Draggable, DragTarget, Page, Row, Text, alignment, border, colors)

def main(page: Page):
    page.title = "Drag and Drop example 2"

    def drag_accept(e):
        # get draggable (source) control by its ID
        src = page.get_control(e.src_id)
        # update text inside draggable control
        tmp = src.content.content.value
        src.content.content.value = e.control.content.content.value
        # reset source group, so it cannot be dropped to a target anymore
        src.group = ""
        # update text inside drag target control
        e.control.content.content.value = tmp
        # reset border
        e.control.content.border = None
        page.update()

    def drag_will_accept(e):
        # black border when it's allowed to drop and red when it's not
        e.control.content.border = border.all(
            2, colors.BLACK45 if e.data == "true" else colors.RED
        )
        e.control.update()

    def drag_leave(e):
        e.control.content.border = None
        e.control.update()

    src = Text("1", size=20)
    page.add(
        Row(
            [
                Draggable(
                    group="number",
                    content=Container(
                        width=50,
                        height=50,
                        bgcolor=colors.CYAN_200,
                        border_radius=5,
                        content=src,
                        alignment=alignment.center,
                    ),
                    content_when_dragging=Container(
                        width=50,
                        height=50,
                        bgcolor=colors.BLUE_GREY_200,
                        border_radius=5,
                    ),
                    content_feedback=Text(src.value),
                ),
                Container(width=100),
                DragTarget(
                    group="number",
                    content=Container(
                        width=50,
                        height=50,
                        bgcolor=colors.PINK_200,
                        border_radius=5,
                        content=Text("0", size=20),
                        alignment=alignment.center,
                    ),
                    on_accept=drag_accept,
                    on_will_accept=drag_will_accept,
                    on_leave=drag_leave,
                ),
            ]
        )
    )

if __name__ == '__main__':
    flet.app(target=main)