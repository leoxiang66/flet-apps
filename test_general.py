import copy

from task_scheduler.model.tasks import *

dictobj = {'name': 'tx', 'age': 25}
a = BaseModel(name='tx', age=25)

# test1
def test1():
    assert vars(a) == dictobj
    assert a.to_dict() == dictobj
    assert BaseModel.from_dict(dictobj) == a


def test_todo():
    a = Todo('todo1', '1 minute')
    b = Todo('todo2', '2 minute')
    assert copy.copy(a) == a
    assert copy.deepcopy(b) == b

    todolist1 = TodoList([a,b])
    todolist2 = TodoList()
    todolist2.addTodos(a)
    todolist2.addTodos(b)

    assert todolist1 == todolist2