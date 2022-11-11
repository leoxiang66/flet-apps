import flet
from flet import Audio, ElevatedButton, Page, Text
import pygame



def main(page: Page):
    pygame.mixer.init()
    pygame.mixer.music.load("./tishi.mp3")

    # audio1 = Audio(
    #     src="https://luan.xyz/files/audio/ambient_c_motion.mp3", autoplay=True
    # )
    # page.overlay.append(audio1)
    # page.add(
    #     Text("This is an app with background audio."),
    #     ElevatedButton("Stop playing", on_click=lambda _: audio1.pause()),
    # )

    pygame.mixer.music.play()


if __name__ == '__main__':
    flet.app(target=main)