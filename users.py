from HW12.validators import *
import requests as rq


class User:
    username = Username_UDescriptor()
    password = Password_UDescriptor()

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def register(cls, username, password):
        return cls(username, password)

    def save(self):
        response = rq.post("http://192.168.1.167:8080/",
                           json={"action": "signin", "username": self.username, "password": self.password})
        return response

    @classmethod
    def login(cls, username, password):
        response = rq.post("http://192.168.1.167:8080/",
                           json={"action": "login", "username": username, "password": password})

        return response.json()["status"]

    @staticmethod
    def get_city(username, city_name):
        response = rq.get(f"http://192.168.1.167:8080/?user={username}&city={city_name}")
        return response
