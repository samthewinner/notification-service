"""
Server

This module contains the server implementation
"""

import uvicorn
from fastapi import FastAPI
from model import Publish, Subscribe, Task, Topic
from task_manager import TaskManager


class Server:
    def __init__(self, task_manager: TaskManager):
        self.app = FastAPI()
        self.task_manager = task_manager
        self.setup_routes()

    def setup_routes(self):
        @self.app.post("/")
        def read_root():
            return {"Hello": "World"}

        @self.app.post("/create/")
        def create_topic(topic: Topic):
            task = Task("create", topic)
            self.task_manager.add_task_sync(task)
            return {"topic created": topic.topic}

        @self.app.post("/delete/")
        def delete_topic(topic: Topic):
            task = Task("delete", topic)
            self.task_manager.add_task_sync(task)
            return {"topic deleted": topic.topic}

        @self.app.post("/publish/")
        def publish(publish: Publish):
            task = Task("publish", publish)
            self.task_manager.add_task_sync(task)
            return {"topic published": publish.topic, "message": publish.message}

        @self.app.post("/subscribe/")
        def subscribe(subscribe: Subscribe):
            task = Task("subscribe", subscribe)
            self.task_manager.add_task_sync(task)
            return {"topic subscribed": subscribe.topic, "subscriber": subscribe.user}

        @self.app.post("/unsubscribe/")
        def unsubscribe(unsubscribe: Subscribe):
            task = Task("unsubscribe", unsubscribe)
            self.task_manager.add_task_sync(task)
            return {
                "topic unsubscribed": unsubscribe.topic,
                "subscriber": unsubscribe.user,
            }

    async def run(self, host: str = "localhost", port: int = 8000):
        # NOTE: This will probably block
        # the event loop, so it's better to
        # use `serve` method instead
        await uvicorn.run(self.app, host=host, port=port)

    async def serve(self, host: str = "localhost", port: int = 8000):
        config = uvicorn.Config(self.app, host=host, port=port)
        server = uvicorn.Server(config)
        await server.serve()
