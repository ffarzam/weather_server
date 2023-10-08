from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import parse_qsl, urlparse
from actions import *
import requests as rq
from database import WeatherDatabase
from server_log import server_logger
from constants import SERVER_HOST, SERVER_PORT, API_RAW_URL, API_KEY


class ConnectionManager:
    def __init__(self, final_url: str):
        self.final_url = final_url

    def __enter__(self):
        self.file = rq.get(self.final_url)
        return self.file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.file.close()


def get_city_weather(city: str) -> dict:
    weather_info = {}
    RAW_URL = API_RAW_URL
    KEY = API_KEY
    final_url = RAW_URL + "?q=" + city + "&appid=" + KEY + "&units=metric"
    try:
        with ConnectionManager(final_url) as response:
            if response:
                weather_info["temperature"] = response.json()["main"]["temp"]
                weather_info["feels_like"] = response.json()["main"]["feels_like"]
                weather_info["last_updated"] = datetime.fromtimestamp(response.json()["dt"]).strftime(
                    "%Y-%m-%d %H:%M:%S")
                return {"status code": response.status_code, "weather_info": weather_info}

            return {"status code": response.status_code, "weather_info": response.json()}
    except Exception as err:
        server_logger.warning(err)


class MyWeatherServer(BaseHTTPRequestHandler):

    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        try:
            query_data = self.query_data()
            choice = query_data["city"]
            username = query_data["user"]
            user_id = get_user_id(database, username)
            if user_id is not None:
                user_id = user_id[0]
                res = database.cache(choice)
                if res:
                    weather_info = {"temperature": float(res[2]), "feels_like": float(res[3]),
                                    "last_updated": res[4].strftime("%Y-%m-%d %H:%M:%S")}
                    weather_info_json = json.dumps(weather_info)
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(weather_info_json.encode("utf-8"))
                    save_request(database, user_id, choice,"200")
                    save_response(database, choice, weather_info)
                else:
                    weather_info = get_city_weather(choice)
                    weather_info_json = json.dumps(weather_info["weather_info"])
                    self.send_response(weather_info["status code"])
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(weather_info_json.encode("utf-8"))

                    if weather_info["status code"] == 200:
                        save_request(database, user_id, choice,weather_info["status code"])
                        save_response(database, choice, weather_info["weather_info"])
                    else:
                        save_request(database, user_id, choice,weather_info["status code"])
            else:
                self.send_response(401)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write("Somthing wrong".encode("utf-8"))
        except Exception as err:
            server_logger.error(err)

    def do_POST(self):
        try:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len)
            post_body_dict = json.loads(post_body)
            if post_body_dict["action"] == "signin":
                save_user(database, post_body_dict["username"], post_body_dict["password"])
                self.wfile.write("You've registered successfully!".encode('utf-8'))

            elif post_body_dict["action"] == "login":
                state = check_login_user(database, post_body_dict["username"], post_body_dict["password"])
                state_json = json.dumps({"status": state})
                self.wfile.write(state_json.encode('utf-8'))
        except Exception as err:
            server_logger.error(err)


def start_server() -> None:

    server = HTTPServer((SERVER_HOST, SERVER_PORT), MyWeatherServer)
    print("Server listening on")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server_logger.info("Stopping Server.")
        server.server_close()
        print("Server closed")

    except Exception as err:
        server_logger.critical(err)
        server.server_close()
        print("Server closed")


if __name__ == "__main__":
    database = WeatherDatabase()
    database.create_tables()
    start_server()
    database.close()
