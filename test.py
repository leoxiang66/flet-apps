if __name__ == '__main__':
    from task_scheduler.task import Task
    task = Task.load_from_json('./.cache/140133042055488.json',None)
    print(task.toDict())