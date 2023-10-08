import re


def validate_password(pwd):
    password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%_^&.*-]).{8,}$"
    match = re.match(password_pattern, pwd)
    return bool(match)
