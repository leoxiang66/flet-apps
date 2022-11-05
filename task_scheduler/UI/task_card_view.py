from typing import Optional, Union, Any
import flet as ft
import threading
from flet import Control, Ref, colors
from flet.control import OptionalNumber
from flet.types import RotateValue, ScaleValue, OffsetValue, AnimationValue, MarginValue
import pygame.mixer as mixer
import time
from pathlib import Path
from ..io.task_card_io import TaskCardIO


SOUND_PATH = str(Path(__file__).absolute().parent.parent) + '/static/tishi.mp3'

# print(SOUND_PATH)



class TaskCard(ft.Card,threading.Thread,TaskCardIO):
    def __init__(self,task_name:str,time: str ,page: ft.Page,content: Optional[Control] = None, ref: Optional[Ref] = None, width: OptionalNumber = None,
                 height: OptionalNumber = None, left: OptionalNumber = None, top: OptionalNumber = None,
                 right: OptionalNumber = None, bottom: OptionalNumber = None, expand: Union[None, bool, int] = None,
                 opacity: OptionalNumber = None, rotate: RotateValue = None, scale: ScaleValue = None,
                 offset: OffsetValue = None, aspect_ratio: OptionalNumber = None,
                 animate_opacity: AnimationValue = None, animate_size: AnimationValue = None,
                 animate_position: AnimationValue = None, animate_rotation: AnimationValue = None,
                 animate_scale: AnimationValue = None, animate_offset: AnimationValue = None, on_animation_end=None,
                 tooltip: Optional[str] = None, visible: Optional[bool] = None, disabled: Optional[bool] = None,
                 data: Any = None, margin: MarginValue = None, elevation: OptionalNumber = None):
        super().__init__(content, ref, width, height, left, top, right, bottom, expand, opacity, rotate, scale, offset,
                         aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale,
                         animate_offset, on_animation_end, tooltip, visible, disabled, data, margin, elevation)

        if 'Minute' in time:
            idx = time.index(' ')
            time_ = 60 * int(time[:idx])
        else:
            time_ = 30

        self.name = task_name
        self.time = time
        self.remaining_time = time_
        self.width = 200
        self.page = page

        if content is None:
            self.content = ft.Checkbox(label= f'''{task_name}: {self.remaining_time}s''', value=False, disabled=True,
                                       fill_color={
                "": colors.CYAN,
            },

                                       )



    def update_content(self):
        self.content.label = f'''{self.name}: {self.remaining_time}s'''
        self.page.update()


    def run(self) -> None:
        while self.remaining_time >0:
            time.sleep(1)
            self.remaining_time -= 1
            self.update_content()
        self.content.value = True
        self.page.update()

        mixer.init()
        mixer.music.load(SOUND_PATH)
        mixer.music.play()

    def toDict(self) -> dict:
        return dict(
            task_name = self.name,
            time = self.time,
        )

