import asyncio
from server import Server
from task_manager import TaskManager

from consts import (
    SELF_PORT
)


async def main():
    task_manager = TaskManager()
    server = Server(task_manager)

    asyncio.create_task(task_manager.run())

    asyncio.create_task(task_manager.wait_for_completion())

    await server.serve(
        host="0.0.0.0",
        port=SELF_PORT
    )

if __name__ == "__main__":
    asyncio.run(main())
