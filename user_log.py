import logging


user_logger = logging.getLogger(__name__)
f_handler = logging.FileHandler("user.log")
f_format = logging.Formatter("%(levelname)s || (%(asctime)s) || %(message)s")
f_handler.setFormatter(f_format)
user_logger.addHandler(f_handler)
user_logger.setLevel(logging.DEBUG)


