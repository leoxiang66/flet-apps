from .base import BaseModel
from typing import Optional,Union,List
from ..utils import convert_time
import asyncio



class Todo(BaseModel):
    def __init__(self, todo_name:str,time: str):
        super().__init__()
        self.todo_name = todo_name
        self.time = time
        self.callback = None

    async def run(self):
        time = convert_time(self.time)
        if self.callback is not None:
            self.callback(time)

        for i in range(time):
            await asyncio.sleep(1)
            if self.callback is not None:
                self.callback(time-i-1)

    def to_dict(self) -> dict:
        return dict(
            todo_name = self.todo_name,
            time = self.time
        )


class TodoList(BaseModel):
    '''
    list of Todos
    '''
    def __init__(self,Todos:Optional[Union[Todo, List[Todo]]]=None) -> None:
        super().__init__()
        self.__list__ = [] # List[Todo]

        if Todos is not None:
            self.addTodos(Todos)

    def addTodos(self, Todos:Union[Todo, List[Todo]]):
        if isinstance(Todos,Todo):
            self.__list__.append(Todos)
        elif isinstance(Todos, list):
            self.__list__ += Todos

    # subscriptable and slice-able
    def __getitem__(self, idx):
        return self.__list__[idx]


    def __str__(self):
        ret = f'There are {len(self.__list__)} Todos:\n'
        for id, Todo in enumerate(self.__list__):
            ret += f'{id+1}) '
            ret += f'{Todo}'

        return ret

    # return an iterator that can be used in for loop etc.
    def __iter__(self):
        return self.__list__.__iter__()

    def __len__(self):
        return len(self.__list__)



class Task(BaseModel):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.todolist = TodoList()

    def add_todo(self,name:str,time:str):
        self.todolist.addTodos(Todo(name,time))

    def getTodos(self) -> List[Todo]:
        return self.todolist.__list__


    def __await__(self):
        for todo in self.todolist:
            yield from todo.run().__await__()
        return 'done'

    def to_dict(self) -> dict:
        return dict(
            name = self.name,
            todos = [x.to_dict() for x in self.getTodos()]
        )

    @classmethod
    def from_json(cls, path: str):
        dict_obj = cls.json_to_dict(path)
        ret = cls(name=dict_obj['name'])
        for i in dict_obj['todos']:
            ret.add_todo(i['todo_name'], i['time'])
        return ret





