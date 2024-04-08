import os
import time
import datetime
import sys
from loguru import logger
from .config import Config

# logger.remove(handler_id=None)
logger.add(
    os.path.expanduser("~/.cache/memest"),
    rotation="00:00",
    retention=datetime.timedelta(days=7),
    backtrace=True,
    diagnose=True,
    enqueue=True,
)
CONFIG_FILE = os.path.expanduser("~/.config/memest/config.ini")


def show_status():
    pass


def do_init():
    pass


def main():
    cfg = Config(CONFIG_FILE)
    logger.info("config file:{}", CONFIG_FILE)
    all_rep = [i for i in cfg.get_sections() if i != "default"]
    logger.info("all_rep: {}", all_rep)
    while True:
        time.sleep(5)
        cfg.update_config()
        break
    print(CONFIG_FILE)
