"""
HTTP Protocol

This module is responsible for handling HTTP requests to the backend server.
"""

import requests

from protocol import Protocol


class HTTPProto(Protocol):
    def __init__(self, url):
        self.url = url

    def get(self, endpoint: str):
        response = requests.get(self.url + endpoint)
        return response

    def post(self, endpoint: str, data: dict):
        response = requests.post(self.url + endpoint, json=data)
        return response
