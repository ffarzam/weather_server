from actions import *
from database import WeatherDatabase


def admin_panel(db) -> None:
    while True:
        print()
        choice = input("1) Get the number of requests so far\n"
                       "2) Get the number of successful requests\n"
                       "3) Get the list of requests in last hour\n"
                       "4) Get the list of requests for each city\n"
                       "5) Exit\n"
                       "-----> ")
        print()

        if choice == "1":

            request_count(db)

        elif choice == "2":

            successful_request_count(db)

        elif choice == "3":

            last_hour_requests(db)

        elif choice == "4":

            city_request_count(db)

        elif choice == "5":
            break


if __name__ == "__main__":
    database = WeatherDatabase()
    admin_panel(database)
    database.close()

