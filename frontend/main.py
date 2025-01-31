import asyncio
from server import Server
from task_manager import TaskManager


async def main():
    task_manager = TaskManager()
    web_service = Server(task_manager)

    asyncio.create_task(task_manager.run())

    await task_manager.wait_for_completion()

    await web_service.serve(
        host="localhost",
        port=8000
    )

asyncio.run(main())
