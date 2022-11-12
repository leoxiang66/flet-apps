from typing import Union
from pprint import pprint

class BaseController:
    CALLBACK = {}

    @classmethod
    def bind_controller(cls, widget_name:str,keywords: list[str] ,functions: list[callable], args: list[tuple]):
        temp = {}
        for i,func,arg in zip(keywords,functions,args):
            def new_func(e):
                func(e,*arg)

            temp[i] = new_func

        cls.CALLBACK[widget_name] = temp
        return temp
    @classmethod
    def get_controllers(cls,widget_name:str) -> Union[dict,None]:
        if widget_name in cls.CALLBACK:
            pprint(cls.CALLBACK[widget_name])
            return cls.CALLBACK[widget_name]
        else:
            return None



BaseController.bind_controller('test',['on_click'],[lambda e: print(1)],[()])

if __name__ == '__main__':
    a = ()
    print(*a)