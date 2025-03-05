"""
Task Manager

The TaskManager class is responsible for managing
tasks that are added to the queue. It processes the
tasks by sending requests to the metadata service and
temporary storage based on the task type.
"""

import asyncio

from consts import (
    METADATA_SERVICE_ENDPOINT,
    TEMPORARY_STORAGE_ENDPOINT,
)
from http_proto import HTTPProto


class TaskManager:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.tasks = []
        self.metadata_service = HTTPProto(METADATA_SERVICE_ENDPOINT)
        self.temporary_storage = HTTPProto(TEMPORARY_STORAGE_ENDPOINT)

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
            self.metadata_service.post('/create/', task.data.dict())
            print("Response: ", "Create topic response")

        elif task.type == 'delete':
            self.metadata_service.post('/delete/', task.data.dict())
            print("Response: ", "Delete topic response")

        elif task.type == 'publish':
            # this will publish a message to a
            # topic on the temporary storage

            # NOTE: When publishing the metadata service
            # returns a list of subscriber ids, we can use lru
            # cache to store the subscriber ids and use it to
            # send the message to the subscribers

            # NOTE: We can use lru_cache to store the subscriber ids
            # import functools
            # @functools.lru_cache(maxsize=3)  # Specify the maximum cache size (3 in this case)
            # def expensive_function(x):
            #     print(f"Calculating for {x}")
            #     return x * x

            # # Calling the function
            # print(expensive_function(1))  # Calculating for 1
            # print(expensive_function(2))  # Calculating for 2
            # print(expensive_function(3))  # Calculating for 3
            # print(expensive_function(1))  # Cached result for 1
            # print(expensive_function(4))  # Calculating for 4, evicts least recently used (2)

            self.metadata_service.post('/publish', task.data.dict())
            print("Response: ", "Publish message response")

        elif task.type == 'subscribe':
            self.metadata_service.post('/subscribe/', task.data.dict())
            print("Response: ", "Subscribe user response")

        elif task.type == 'unsubscribe':
            self.metadata_service.post('/unsubscribe/', task.data.dict())
            print("Response: ", "Unsubscribe user response")

        else:
            raise ValueError(f"Invalid task type: {task.type}")
