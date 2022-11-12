from task_scheduler.model.tasks import *


if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor

    task = Task('1')
    task.add_todo('todo1', '1 sss')
    task.add_todo('todo2', '1 sdf')


    task2 = Task('2')
    task2.add_todo('SSS', '11')
    task2.add_todo('sdfsdf','sdf')


    async def task_listener(prompt: str = ''):
        while True:
            with ThreadPoolExecutor(1, 'ainput') as executor:
                tmp = await asyncio.get_event_loop().run_in_executor(executor, input, prompt)
                task3 = Task(tmp)
                task3.add_todo('中国牛逼','1')
                print(tmp.upper())
                await task3


    async def event_loop():
        await asyncio.gather(task.__await__(), task2.__await__(), task_listener('输入')
                             )  # gatter函数首先将这3个courotine object包装成3个tasks， 并将他们加入到event loop中

    asyncio.run(event_loop())

    print('done')