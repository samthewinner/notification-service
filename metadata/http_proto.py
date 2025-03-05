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
        try:
            response = requests.get(self.url + endpoint)
        except Exception as e:
            print(f"Error occurred while sending GET request: {e}")
            return {"status": "failed", "error": str(e)}
        return response

    def post(self, endpoint: str, data: dict):
        try:
            response = requests.post(self.url + endpoint, json=data)
        except Exception as e:
            print(f"Error occurred while sending POST request: {e}")
            return {"status": "failed", "error": str(e)}
        return response
