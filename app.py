if __name__ == '__main__':
    from task_scheduler.view.pages  import HomePage
    from task_scheduler.view.widgets import *
    import flet as ft


    def main(page:ft.Page):
        page.horizontal_alignment = 'center'
        page.add(ft.Markdown('# Task Scheduler'))
        page.title = 'Task Scheduler'
        page.scroll = 'adaptive'
        page.window_width = 1000
        page.window_height = 500
        homepage = HomePage(page, 3)



        a = TaskWidget(page)
        homepage.task_widget = a
        homepage.append_widget(a.to_flet(), 0)

        homepage.refresh()





    ft.app(target=main,
           # view=ft.WEB_BROWSER
           )

