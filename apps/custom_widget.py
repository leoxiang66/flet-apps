from flet import *

class Countdown(UserControl):
    def __init__(self, seconds):
        super().__init__()
        self.seconds = seconds

    def did_mount(self):
        self.running = True
        self.th = threading.Thread(target=self.update_timer, args=(), daemon=True)
        self.th.start()

    def will_unmount(self):
        self.running = False

    def update_timer(self):
        while self.seconds and self.running:
            mins, secs = divmod(self.seconds, 60)
            self.countdown.value = "{:02d}:{:02d}".format(mins, secs)
            self.update()
            time.sleep(1)
            self.seconds -= 1

    def build(self):
        self.countdown = Text()
        return self.countdown

def main(page):
    page.add(Countdown(120), Countdown(60))

if __name__ == '__main__':
    flet.app(target=main)