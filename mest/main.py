import os
import sys
import time
import datetime
import subprocess

import psutil
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
USAGE = """ USAGE memest [cmd]
cmd: start, status, stop
"""


def show_status():
    pass


def do_init():
    pass


def is_memest_daemon_running():
    for process in psutil.process_iter(["pid", "name", "cmdline"]):
        cmdline = " ".join(process.info['cmdline'])
        if "--daemon" in cmdline and "memest" in cmdline:
            return True
    return False


def stop_memest_daemon():
    pass


def run_forever():
    cfg = Config(CONFIG_FILE)
    logger.info("config file: {}", CONFIG_FILE)
    all_rep = [i for i in cfg.get_sections() if i != "default"]
    logger.info("all_rep: {}", all_rep)
    while True:
        if cfg.update_config():
            all_rep = [i for i in cfg.get_sections() if i != "default"]
            logger.info("all_rep: {}", all_rep)
        time.sleep(5)


def main():
    if len(sys.argv) < 2:
        print(USAGE)
        exit(1)
    cmd = sys.argv[1]
    if cmd == "start":
        if is_memest_daemon_running():
            logger.info("memest is running")
        else:
            logger.info("start memest")
            os.system('nohup memest --daemon >> /dev/null 2>&1 &')
            logger.info("start memest")
            return
    if cmd == "status":
        if is_memest_daemon_running():
            logger.info("memest is running")
        else:
            logger.info("memest is dead")
    if cmd == "--daemon":
        run_forever()
