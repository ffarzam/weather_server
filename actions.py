from datetime import datetime
from HW12.users import User


def sign_in():
    username = input("username: ")
    password = input("password: ")

    user = User.register(username, password)
    return user


def send_user(user):
    return user.save()


def is_logged_in(username, password):
    return User.login(username, password)


def check_login_user(db, username, password):
    return db.login_user(username, password)


def table_creation(db):
    db.create_tables()


def get_request(username, city_name):
    response = User.get_city(username, city_name)
    return response


def show(response):
    for i, j in response.json().items():
        print('\033[31m' f"{i} : {j}" '\033[m')


def get_user_id(db, username):
    return db.get_user(username)


def save_user(db, username, password):
    db.set_user(username, password)


def save_request(db, user_id, city_name,status_code):
    db.save_request_data(user_id, city_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),status_code)


def save_response(db, city_name, response):
    db.save_response_data(city_name, response)


def get_weather_info(username):
    while True:
        city_name = input('\033[32m' "Enter city name: "'\033[m').lower()
        response = get_request(username, city_name)
        if response.status_code == 200:
            show(response)
            break
        elif response.status_code == 404:
            print('\033[31m' "Error retrieving weather data: No matching location found."'\033[m')


def request_count(db):
    print('\033[35m' f"Number of requests so far: {db.get_request_count()}"'\033[m')


def successful_request_count(db):
    print('\033[35m' f"Number of successful requests so far: {db.get_successful_request_count()}" '\033[m')


def last_hour_requests(db):
    lst = db.get_last_hour_requests()
    for item in lst:
        print('\033[32m', f"{item[1]:25}{item[3]:35}{item[2]}", '\033[m')
        print()


def city_request_count(db):
    lst = db.get_city_request_count()
    for item in lst:
        print('\033[32m', f"{item[0]:25}{item[1]}", '\033[m')
        print()
