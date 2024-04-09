import os
import sys
import time
import signal
import datetime
import subprocess

import psutil
from loguru import logger

from .config import Config
from .rep_mana import MeST

# logger.remove(handler_id=None)
logger.add(
    os.path.expanduser("~/.cache/memest"),
    rotation="00:00",
    retention=datetime.timedelta(days=7),
    backtrace=True,
    diagnose=True,
    enqueue=True,
)
USAGE = """ USAGE memest [cmd]
cmd: start, status, stop
"""


def is_memest_daemon_running():
    for process in psutil.process_iter(["pid", "name", "cmdline"]):
        cmdline = " ".join(process.info['cmdline'])
        if "--daemon" in cmdline and "memest" in cmdline:
            return True
    return False


def stop_memest_daemon():
    for process in psutil.process_iter(["pid", "name", "cmdline"]):
        cmdline = " ".join(process.info['cmdline'])
        if "--daemon" in cmdline and "memest" in cmdline:
            os.kill(process.info['pid'], signal.SIGKILL)


def run_forever():
    CONFIG_FILE = os.path.expanduser("~/.config/memest/config.ini")
    cfg = Config(CONFIG_FILE)
    logger.info("config file: {}", CONFIG_FILE)
    mestor = MeST(cfg)
    mestor.run()


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
    elif cmd == "status":
        if is_memest_daemon_running():
            print("memest is running")
        else:
            print("memest is dead")
    elif cmd == 'stop':
        stop_memest_daemon()
    elif cmd == "--daemon":
        run_forever()
