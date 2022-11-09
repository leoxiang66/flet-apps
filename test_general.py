import copy

from task_scheduler.model.tasks import *

dictobj = {'name': 'tx', 'age': 25}
basemodel = BaseModel(name='tx', age=25)

todo1 = Todo('todo1', '1 minute')
todo2 = Todo('todo2', '2 minute')

task1 = Task('task1')
task1.add_todo('todo1', '1 minute')

# test1
def test1():
    assert vars(basemodel) == dictobj
    assert basemodel.to_dict() == dictobj
    assert BaseModel.from_dict(dictobj) == basemodel


def test_todo():

    assert copy.copy(todo1) == todo1
    assert copy.deepcopy(todo2) == todo2

    todolist1 = TodoList([todo1, todo2])
    todolist2 = TodoList()
    todolist2.addTodos(todo1)
    todolist2.addTodos(todo2)

    assert todolist1 == todolist2

def test_tasks():
    assert task1.getTodos()[0] == todo1