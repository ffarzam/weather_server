import logging


server_logger = logging.getLogger(__name__)
f_handler = logging.FileHandler("server.log")
f_format = logging.Formatter("%(levelname)s || (%(asctime)s) || %(message)s || (line: %(lineno)d [%(filename)s])")
f_handler.setFormatter(f_format)
server_logger.addHandler(f_handler)
server_logger.setLevel(logging.DEBUG)

