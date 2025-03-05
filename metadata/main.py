"""
Metadata Service

This service will have a sqlite database to store the topics and associated subscribers.
And it will have a REST API server and a Task Queue to handle the requests.
"""

import asyncio
from server import Server
from task_manager import TaskManager


async def main():
    task_manager = TaskManager()
    server = Server(task_manager)

    asyncio.create_task(task_manager.run())

    asyncio.create_task(task_manager.wait_for_completion())

    await server.serve(
        host="0.0.0.0",
        port=9000
    )

if __name__ == "__main__":
    asyncio.run(main())
