from .base import BaseModel
from typing import Optional,Union,List

class Todo(BaseModel):
    def __init__(self, todo_name:str,time: str):
        super().__init__()
        self.todo_name = todo_name
        self.time = time


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