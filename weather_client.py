from actions import *
import user_log


def start_client() -> None:
    while True:
        print()
        choice = input("1) sign up\n"
                       "2) sign in\n"
                       "3) Exit\n"
                       "-----> ")
        print()

        if choice == "1":
            try:
                user = sign_in()
                res = send_user(user)
                print(res.text)
                user_log.user_logger.error(f"{user.username} signed up")

            except Exception as err:
                print(err)
                user_log.user_logger.error(err)

        elif choice == "2":
            username = input("username: ")
            password = input("password: ")
            try:
                if is_logged_in(username, password):
                    print("\nLogged in successfully\n")
                    user_log.user_logger.info(f"{username} logged in")
                    while True:
                        do_what = input("What do you want to do?\n"
                                        "1)Get Weather Information\n"
                                        "2)Exit\n"
                                        "-----> ")

                        if do_what == "1":
                            get_weather_info(username)

                        elif do_what == "2":
                            user_log.user_logger.info(f"{username} logged out")
                            break
                else:
                    print("Username & Password don't match")
            except Exception as err:
                user_log.user_logger.error(err)

        elif choice == "3":
            break


if __name__ == "__main__":
    try:
        start_client()
    except KeyboardInterrupt:
        user_log.user_logger.info("Stopping the weather client")

    # Langarūd
