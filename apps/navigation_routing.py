import flet
from flet import *
from flet import colors

def main(page: Page):
    page.add(Text(f"Initial route: {page.route}"))



def main2(page: Page):
    page.add(Text(f"Initial route: {page.route}"))

    def route_change(route):
        page.add(Text(f"New route: {route}"))

    page.on_route_change = route_change
    page.update()



def main3(page: Page):
    page.add(Text(f"Initial route: {page.route}"))

    def route_change(route):
        page.add(Text(f"New route: {route}"))

    def go_store(e):
        page.route = "/store"
        page.update()

    page.on_route_change = route_change
    page.add(ElevatedButton("Go to Store", on_click=go_store))



def main4(page: Page):
    page.title = "Routes Example"
    home_view = View(
                "/",
                [
                    AppBar(title=Text("Flet app"), bgcolor=colors.SURFACE_VARIANT),
                    ElevatedButton("Visit Store", on_click=lambda _: page.go("/store")),
                ],
            )

    store_view = View(
                    "/store",
                    [
                        AppBar(title=Text("Store"), bgcolor=colors.SURFACE_VARIANT),
                        ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )

    def route_change(route):
        page.views.clear()
        page.views.append(
            home_view
        )
        if page.route == "/store":
            page.views.append(
                store_view
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)





if __name__ == '__main__':
    # flet.app(target=main)
    # flet.app(target=main2, view=flet.WEB_BROWSER)
    # flet.app(target=main3, view=flet.WEB_BROWSER)
    flet.app(target=main4, view=flet.WEB_BROWSER)