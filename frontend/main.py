import asyncio
from server import Server
from task_manager import TaskManager


async def main():
    task_manager = TaskManager()
    web_service = Server(task_manager)

    asyncio.create_task(task_manager.run())

    await task_manager.wait_for_completion()

    await web_service.serve(
        host="0.0.0.0",
        port=8000
    )

if __name__ == "__main__":
    asyncio.run(main())
