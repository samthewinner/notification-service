"""
This module contains the models used for communication
between frontend and metadata service.
"""

from pydantic import BaseModel
from uuid import UUID


class User(BaseModel):
    """
    User model

    Attributes
    ----------
    id : uuid4
        The unique identifier of the user
    name : str
        The name of the user
    """
    id: str
    name: str


class Topic(BaseModel):
    """
    Topic model

    Attributes
    ----------
    topic: str
        The name of the topic
    """
    topic: str


class Publish(BaseModel):
    """
    Publish model

    Attributes
    ----------
    topic: str
        The name of the topic
    message : str
        The message to be published
    """
    topic: str
    message: str


class Subscribe(BaseModel):
    """
    Subscribe model

    Attributes
    ----------
    topic: str
        The name of the topic
    user : User
        The user to subscribe
    """
    topic: str
    user: User


class Task:
    """
    Task model

    Attributes
    ----------
    type : str
        The type of the task
    data : Topic | Publish | Subscribe | User
        The data of the task
    """
    def __init__(self, type: str, data: Topic | Publish | Subscribe | User):
        self.type = type
        self.data = data
