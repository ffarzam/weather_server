from HW12.database import WeatherDatabase
from HW12.utils import *


class Username_UDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        db = WeatherDatabase()

        if 4 >= len(value) or len(value) > 24:
            raise TypeError("Username must contain more than 4 char and less than 24 char")
        elif db.check_username(value) is not None:
            raise TypeError("Username already exist!")

        instance.__dict__[self.name] = value


class Password_UDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not validate_password(value):
            raise ValueError("Passwords must be at least 8 characters in length,\nand it must include at least one "
                             "capital letter (or uppercase), one lowercase, one number and one special character")
        instance.__dict__[self.name] = value
