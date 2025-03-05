"""
MongoDB schema
- users: table to store user information
- user_to_topics: table to store the topics subscribed by the user
- topic_to_users: table to store the users subscribed to the topic

APIs
- subscribe: API to subscribe to a topic
    - will create a new user if the user does not exist
    - will add to user_to_topics and topic_to_users
- unsubscribe: API to unsubscribe from a topic
    - will remove the user from user_to_topics and topic_to_users
- create_topic: API to create a new topic
    - will add the topic to the topics table
- delete_topic: API to delete a topic
    - will remove the topic from the topics table

Schema
users:
    - id: str
    - name: str
user_to_topics:
    - user_id: str
    - topic_id: [str]
topic_to_users:
    - topic_id: str
    - user_id: [str]
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from consts import MONGODB_HOST, MONGODB_PORT
from typing import Optional
import threading
from concurrent.futures import ThreadPoolExecutor


class DBConnection:
    _instance: Optional['DBConnection'] = None
    _lock = threading.Lock()  # Lock for thread-safety

    def __new__(
        cls,
        db_name: str = 'test',
        db_host: str = MONGODB_HOST,
        db_port: int = MONGODB_PORT
    ):
        with cls._lock:  # Ensure thread-safety
            if cls._instance is None:
                cls._instance = super(DBConnection, cls).__new__(cls)
                cls._instance.client = AsyncIOMotorClient(
                    f'mongodb://{db_host}:{db_port}/')
                cls._instance.db = cls._instance.client[db_name]

                # Check if the connection was successful
                try:
                    # Attempt to ping the MongoDB server
                    cls._instance.client.admin.command('ping')
                    print(
                        f"Successfully connected to MongoDB at {db_host}:{db_port}")
                except Exception as e:
                    print(f"Failed to connect to MongoDB: {e}")
                    cls._instance = None  # Reset instance if connection fails
                    raise ConnectionError(
                        f"Unable to connect to MongoDB at {db_host}:{db_port}") from e

                cls._instance.db = cls._instance.client[db_name]
        return cls._instance

    def get_client(self):
        return self.client

    def get_database(self):
        return self.db

    async def create_topic(self, topic: str):
        data = {
            "_id": topic,
            "subscribers": []
        }
        try:
            result = await self.db.topic_to_users.insert_one(data)
            return {"status": "success", "inserted_id": result.inserted_id}
        except Exception as e:
            print(f"Error while creating topic in DB: {e}")
            raise  # Re-raise exception for handling higher up the stack

    async def delete_topic(self, topic_id: str):
        try:
            topic_data = await self.db.topic_to_users.find_one(
                {"_id": topic_id},
            )

            if not topic_data:
                print(f"Topic '{topic_id}' does not exist.")
                return

            subscribers = topic_data.get('subscribers', [])

            for user_id in subscribers:
                self.db.user_to_topics.update_one(
                    {'_id': user_id},
                    {'$pull': {'topics': topic_id}},
                )

            self.db.topic_to_users.delete_one({'_id': topic_id})
            return {"status": "success"}
        except Exception as e:
            print(f"Error while deleting topic in DB: {e}")
            raise

    async def check_topic_exists(self, topic: str):
        try:
            result = await self.db.topic_to_users.find_one({'_id': topic})
            print("Topic Check result: ", result)
            return result is not None
        except Exception as e:
            print(f"Error while checking topic in DB: {e}")
            raise

    async def subscribe(self, topic_id: str, user_id: str):
        try:
            await self.db.topic_to_users.update_one(
                {"_id": topic_id},
                {"$addToSet": {"subscribers": user_id}},
                upsert=True
            )

            await self.db.user_to_topics.update_one(
                {"_id": user_id},
                {"$addToSet": {"topics": topic_id}},
                upsert=True
            )
            return {"status": "success"}
        except Exception as e:
            print(f"Error while subscribing user to topic in DB: {e}")
            raise

    async def unsubscribe(self, user_id: str, topic_id: str):
        try:
            # remove the user from the list of subscribers
            await self.db.topic_to_users.update_one(
                {"_id": topic_id},
                {"$pull": {"subscribers": user_id}}
            )

            # remove the topic from the user's list of topics
            await self.db.user_to_topics.update_one(
                {"_id": user_id},
                {"$pull": {"topics": topic_id}}
            )
            return {"status": "success"}
        except Exception as e:
            print(f"Error while unsubscribing user from topic in DB: {e}")
            raise

    def publish(self, topic_id: str, message: str):
        ...

    def get_subscribers(self, topic_id: str):
        return self.db.topic_to_users.find_one(
            {"_id": topic_id}
        ).get('subscribers', [])

    def get_topics(self, user_id: str):
        return self.db.user_to_topics.find_one(
            {"_id": user_id}
        ).get('topics', [])
