import flet
from flet import Column, ElevatedButton, Page, Row, Text, TextField

def main(page: Page):
    page.title = "Flet Chat"

    # subscribe to broadcast messages
    def on_message(msg):
        messages.controls.append(Text(msg))
        page.update()

    page.pubsub.subscribe(on_message)

    def send_click(e):
        page.pubsub.send_all(f"{user.value}: {message.value}")
        # clean up the form
        message.value = ""
        page.update()

    messages = Column()
    user = TextField(hint_text="Your name", width=150)
    message = TextField(hint_text="Your message...", expand=True)  # fill all the space
    send = ElevatedButton("Send", on_click=send_click)
    page.add(messages, Row(controls=[user, message, send]))

if __name__ == '__main__':
    flet.app(target=main, view=flet.WEB_BROWSER)