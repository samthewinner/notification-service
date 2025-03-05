"""
Task Manager

The TaskManager class is responsible for managing
tasks that are added to the queue. It processes the
tasks by sending requests to the metadata service and
temporary storage based on the task type.
"""

import asyncio

from consts import (
    FRONT_END_SERVICE_ENDPOINT,
)
from http_proto import HTTPProto
from db_api import DBConnection


class TaskManager:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.tasks = []
        self.frontend_service = HTTPProto(FRONT_END_SERVICE_ENDPOINT)
        self.db_client = DBConnection()

    def add_task_sync(self, task):
        self.queue.put_nowait(task)

    async def add_task(self, task):
        await self.queue.put(task)

    async def start_tasks(self):
        while True:
            # Wait for a task to be available in the queue
            task = await self.queue.get()
            # Start the task and store the future
            future = asyncio.create_task(self.process_task(task))
            self.tasks.append(future)
            self.queue.task_done()
            # If the queue is empty, break the loop to exit
            if self.queue.empty():
                break

    async def wait_for_completion(self):
        # Wait for all tasks to complete
        if self.tasks:
            await asyncio.gather(*self.tasks)

    async def run(self):
        # Continuously start tasks as they are added
        while True:
            await self.start_tasks()
            # Allow for a small delay to prevent busy waiting
            await asyncio.sleep(0.1)

    async def process_task(self, task):
        if task.type == 'create':
            try:
                topic_id = task.data.topic
                if await self.db_client.check_topic_exists(topic_id):
                    print("Response", "Topic exist")
                    return {"status": "success"}
                result = await self.db_client.create_topic(topic_id)
                print("Response", "Created topic:", result)  # If successful, this will be printed
                return {"status": "success"}
            except Exception as e:
                print(f"Error occurred while creating topic: {e}")
                return {"status": "failed", "error": str(e)}

        elif task.type == 'delete':
            try:
                topic_id = task.data.topic
                if not await self.db_client.check_topic_exists(topic_id):
                    print("Response", "Topic doesn't exist")
                    return {"status": "success"}
                result = await self.db_client.delete_topic(task.data.dict())
                # self.frontend_service.post('/delete', task.data.dict())
                print("Response", "Deleted topic:", result)
                return {"status": "success"}
            except Exception as e:
                print(f"Error occured while deleting topic: {e}")
                return {"status": "failed", "error": str(e)}

        elif task.type == 'publish':
            topic_id = task.data.topic
            message = task.data.message
            result = await self.db_client.publish(topic_id, message)
            print("Response", "Published message")
            return {"status": "success"}

        elif task.type == 'subscribe':
            topic_id = task.data.topic
            user_id = task.data.user.id
            result = await self.db_client.subscribe(topic_id, user_id)
            print("Response", "Subscribed user")
            return {"status": "success"}

        elif task.type == 'unsubscribe':
            topic_id = task.data.topic
            user_id = task.data.user.id
            result = await self.db_client.unsubscribe(user_id, topic_id)
            print("Response", "Unsubscribed user")
            return {"status": "success"}

        else:
            raise ValueError(f"Invalid task type: {task.type}")
