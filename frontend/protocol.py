"""
This file contains the Protocol class which is an abstract
class that defines the methods that all protocols must implement.
"""

from abc import ABC, abstractmethod


class Protocol(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get():
        pass

    @abstractmethod
    def post():
        pass
