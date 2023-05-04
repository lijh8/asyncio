# logging2.py
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

DEBUG    = logging.debug
INFO     = logging.info
WARNING  = logging.warning
ERROR    = logging.error
CRITICAL = logging.critical

def logging2_init():
    filename = './hello.log'
    size = 10 * 1024 * 1024  # 10M
    count = 10
    level = logging.DEBUG

    fmt = "%(message)s"

    # enable for debug
    # fmt = "%(asctime)s %(levelname)s " \
    #     " %(pathname)s:%(lineno)d:%(funcName)s: %(message)s"

    path = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(path, filename)
    file_handler = RotatingFileHandler(file,
                                        maxBytes=size,
                                        backupCount=count)
    console_handler = logging.StreamHandler(sys.stdout)
    handlers = [file_handler, console_handler]
    logging.basicConfig(handlers=handlers, level=level, format=fmt)

"""
    import logging
    from logging2 import *
    logging2_init()

    logging.debug("")
    logging.info("")
    logging.warning("")
    logging.error("")
    logging.critical("")

    DEBUG("")
    INFO("")
    WARNING("")
    ERROR("")
    CRITICAL("")
"""

