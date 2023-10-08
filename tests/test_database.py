import pytest
from HW12.database import WeatherDatabase
import datetime


@pytest.fixture
def db():
    db = WeatherDatabase(dbname="test")
    yield db
    cursor = db.conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS responses;''')
    cursor.execute('''DROP TABLE IF EXISTS requests;''')
    cursor.execute('''DROP TABLE IF EXISTS users;''')
    db.conn.commit()


def test_create_tables(db):
    db.create_tables()
    cursor = db.conn.cursor()

    cursor.execute('''SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public' AND table_type = 'BASE TABLE';''')

    tables = [table[0] for table in cursor.fetchall()]

    assert 'requests' in tables
    assert 'responses' in tables


def test_set_user(db):
    db.create_tables()
    username = "ffarzam"
    password = "Ffarzam_1992"
    db.set_user(username, password)

    cursor = db.conn.cursor()
    cursor.execute("SELECT username FROM users;")
    row = cursor.fetchone()

    assert row[0] == username


def test_login_user(db):
    db.create_tables()
    cursor = db.conn.cursor()
    username = "ffarzam"
    password = "Ffarzam_1992"
    cursor.execute(
        f"""INSERT INTO Users(username,password) VALUES ('{username}',crypt('{password}', gen_salt('bf')));""")
    db.conn.commit()

    username1 = "fffarzam"
    password1 = "Fffarzam_1992"
    cursor.execute(
        f"""INSERT INTO Users(username,password) VALUES ('{username1}',crypt('{password1}', gen_salt('bf')));""")
    db.conn.commit()

    assert db.login_user(username, password) is True
    assert db.login_user(username1, password) is False


def test_check_username(db):
    db.create_tables()
    cursor = db.conn.cursor()
    username = "ffarzam"
    password = "Ffarzam_1992"
    cursor.execute(
        f"""INSERT INTO Users(username,password) VALUES ('{username}',crypt('{password}', gen_salt('bf')));""")
    db.conn.commit()
    username1 = "fffarzam"
    assert db.check_username(username)[0] == username
    assert db.check_username(username1) is None


def test_get_user(db):
    db.create_tables()
    cursor = db.conn.cursor()
    username = "ffarzam"
    password = "Ffarzam_1992"
    cursor.execute(
        f"""INSERT INTO Users(username,password) VALUES ('{username}',crypt('{password}', gen_salt('bf')));""")
    db.conn.commit()

    username1 = "fffarzam"
    assert db.get_user(username)[0] == 1
    assert db.get_user(username1) is None


def test_save_request_data(db):
    db.create_tables()
    cursor = db.conn.cursor()
    username = "ffarzam"
    password = "Ffarzam_1992"
    cursor.execute(
        f"""INSERT INTO Users(username,password) VALUES ('{username}',crypt('{password}', gen_salt('bf')));""")
    db.conn.commit()

    user_id = 1
    city_name = "rasht"
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_code = '200'

    db.save_request_data(user_id, city_name, request_time, status_code)

    cursor = db.conn.cursor()
    cursor.execute("SELECT * FROM requests;")
    row = cursor.fetchone()

    assert row[1] == user_id
    assert row[2] == city_name
    assert row[3] == datetime.datetime.strptime(request_time, "%Y-%m-%d %H:%M:%S")
    assert row[4] == int('200')


def test_save_response_data(db):
    db.create_tables()
    cursor = db.conn.cursor()
    username = "ffarzam"
    password = "Ffarzam_1992"
    cursor.execute(
        f"""INSERT INTO Users(username,password) VALUES ('{username}',crypt('{password}', gen_salt('bf')));""")
    db.conn.commit()

    user_id = 1
    cursor = db.conn.cursor()
    city_name = "rasht"
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_code = '200'
    cursor.execute(f"""INSERT INTO requests(user_id,city,request_time,status_code) 
                            VALUES ({user_id},'{city_name}', '{request_time}', '{status_code}');""")
    city_name = "rasht"
    temperature = 30.5
    feels_like_temperature = 28.4
    last_update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    weather_info = {'temperature': temperature, 'feels_like': feels_like_temperature, 'last_updated': last_update_time}

    db.save_response_data(city_name, weather_info)

    cursor = db.conn.cursor()
    cursor.execute("SELECT * FROM responses;")
    row = cursor.fetchone()

    assert row[2] == city_name
    assert float(row[3]) == temperature
    assert float(row[4]) == feels_like_temperature
    assert row[5] == datetime.datetime.strptime(last_update_time, "%Y-%m-%d %H:%M:%S")


def test_get_request_count(db):
    db.create_tables()

    cursor = db.conn.cursor()
    username = "ffarzam"
    password = "Ffarzam_1992"
    cursor.execute(
        f"""INSERT INTO Users(username,password) VALUES ('{username}',crypt('{password}', gen_salt('bf')));""")
    db.conn.commit()

    user_id = 1
    cursor = db.conn.cursor()
    city_name = "rasht"
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_code = '200'
    cursor.execute(f"""INSERT INTO requests(user_id,city,request_time,status_code) 
                                VALUES ({user_id},'{city_name}', '{request_time}', '{status_code}');""")

    assert db.get_request_count() == 1


def test_get_successful_request_count(db):
    db.create_tables()

    cursor = db.conn.cursor()
    username = "ffarzam"
    password = "Ffarzam_1992"
    cursor.execute(
        f"""INSERT INTO Users(username,password) VALUES ('{username}',crypt('{password}', gen_salt('bf')));""")
    db.conn.commit()

    user_id = 1
    cursor = db.conn.cursor()
    city_name = "invalid"
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_code = '404'
    cursor.execute(f"""INSERT INTO requests(user_id,city,request_time,status_code) 
                                VALUES ({user_id},'{city_name}', '{request_time}', '{status_code}');""")
    db.conn.commit()

    username = "fffarzam"
    password = "Fffarzam_1992"
    db.set_user(username, password)
    user_id = 2
    city_name = "tehran"
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_code = '200'
    cursor.execute(f"""INSERT INTO requests(user_id,city,request_time,status_code) 
                                VALUES ({user_id},'{city_name}', '{request_time}', '{status_code}');""")
    db.conn.commit()

    city_name = "tehran"
    temperature = 30.0
    feels_like_temperature = 28.4
    last_update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    weather_info = {'temperature': temperature, 'feels_like': feels_like_temperature, 'last_updated': last_update_time}

    cursor.execute(f'''INSERT INTO responses(request_id,city,temperature,feels_like_temperature,last_updated_time)
        VALUES (
        (SELECT last_value FROM requests_id_seq),
        '{city_name}',
        {weather_info['temperature']},
        {weather_info['feels_like']},
        '{weather_info['last_updated']}');''')
    db.conn.commit()

    assert db.get_successful_request_count() == 1


def test_get_last_hour_requests(db):
    db.create_tables()

    cursor = db.conn.cursor()
    username = "ffarzam"
    password = "Ffarzam_1992"
    cursor.execute(
        f"""INSERT INTO Users(username,password) VALUES ('{username}',crypt('{password}', gen_salt('bf')));""")
    db.conn.commit()

    user_id = 1
    city_name = "tehran"
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_code = '200'
    cursor.execute(f"""INSERT INTO requests(user_id,city,request_time,status_code) 
                                VALUES ({user_id},'{city_name}', '{request_time}', '{status_code}');""")
    db.conn.commit()

    cursor = db.conn.cursor()
    username = "fffarzam"
    password = "Fffarzam_1992"
    cursor.execute(
        f"""INSERT INTO Users(username,password) VALUES ('{username}',crypt('{password}', gen_salt('bf')));""")
    db.conn.commit()

    user_id1 = 2
    city_name1 = "rasht"
    request_time1 = "2023-04-08 23:11:11"
    status_code1 = '200'
    cursor.execute(f"""INSERT INTO requests(user_id,city,request_time,status_code) 
                                VALUES ({user_id1},'{city_name1}', '{request_time1}', '{status_code1}');""")
    db.conn.commit()

    lst = db.get_last_hour_requests()

    assert lst[-1] == (user_id, city_name, int(status_code), request_time)
    assert len(lst) == 1


def test_get_city_request_count(db):
    db.create_tables()
    cursor = db.conn.cursor()

    user_id = 1
    username = "ffarzam"
    password = "Ffarzam_1992"
    cursor.execute(
        f"""INSERT INTO Users(username,password) VALUES ('{username}',crypt('{password}', gen_salt('bf')));""")
    db.conn.commit()

    city_name = "rasht"
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # cursor = db.conn.cursor()
    status_code = '200'
    cursor.execute(f"""INSERT INTO requests(user_id,city,request_time,status_code) 
                                VALUES ({user_id},'{city_name}', '{request_time}', '{status_code}');""")
    db.conn.commit()
    lst = db.get_city_request_count()
    for item in lst:
        if item[0] == city_name:
            count = item[1]

    assert count == 1


def test_cache(db):
    db.create_tables()
    cursor = db.conn.cursor()
    user_id = 1
    username = "ffarzam"
    password = "Ffarzam_1992"
    cursor.execute(
        f"""INSERT INTO Users(username,password) VALUES ('{username}',crypt('{password}', gen_salt('bf')));""")
    db.conn.commit()

    city_name = "rasht"
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # cursor = db.conn.cursor()
    status_code = '200'
    cursor.execute(f"""INSERT INTO requests(user_id,city,request_time,status_code) 
                                VALUES ({user_id},'{city_name}', '{request_time}', '{status_code}');""")
    db.conn.commit()

    temperature = 30.0
    feels_like_temperature = 28.4
    last_update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    weather_info = {'temperature': temperature, 'feels_like': feels_like_temperature, 'last_updated': last_update_time}

    cursor.execute(f'''INSERT INTO responses(request_id,city,temperature,feels_like_temperature,last_updated_time)
            VALUES (
            (SELECT last_value FROM requests_id_seq),
            '{city_name}',
            {weather_info['temperature']},
            {weather_info['feels_like']},
            '{weather_info['last_updated']}');''')
    db.conn.commit()

    city_name1 = "tehran"
    request_time1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # cursor = db.conn.cursor()
    status_code = '200'
    cursor.execute(f"""INSERT INTO requests(user_id,city,request_time,status_code) 
                                VALUES ({user_id},'{city_name}', '{request_time}', '{status_code}');""")
    db.conn.commit()

    temperature1 = 31.0
    feels_like_temperature1 = 29.4
    last_update_time1 = "2023-04-08 23:11:11"
    weather_info1 = {'temperature': temperature1, 'feels_like': feels_like_temperature1,
                     'last_updated': last_update_time1}

    cursor.execute(f'''INSERT INTO responses(request_id,city,temperature,feels_like_temperature,last_updated_time)
                VALUES (
                (SELECT last_value FROM requests_id_seq),
                '{city_name1}',
                {weather_info1['temperature']},
                {weather_info1['feels_like']},
                '{weather_info1['last_updated']}');''')
    db.conn.commit()

    lst = db.cache(city_name)
    lst1 = db.cache(city_name1)

    assert lst[0] == user_id
    assert lst[1] == city_name
    assert float(lst[2]) == temperature
    assert float(lst[3]) == feels_like_temperature
    assert lst[4] == datetime.datetime.strptime(last_update_time, "%Y-%m-%d %H:%M:%S")
    assert lst1 is None
