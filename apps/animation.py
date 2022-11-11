import flet
from flet import Container, ElevatedButton, Page

def main(page: Page):

    c = Container(
        width=150,
        height=150,
        bgcolor="blue",
        border_radius=10,
        animate_opacity=300,
    )

    def animate_opacity(e):
        c.opacity = 0 if c.opacity == 1 else 1
        c.update()

    page.add(
        c,
        ElevatedButton(
            "Animate opacity",
            on_click=animate_opacity,
        ),
    )

if __name__ == '__main__':
    flet.app(target=main)