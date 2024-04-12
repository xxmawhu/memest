import os
from pprint import pprint
import sys
import time
import signal
import datetime
import subprocess

import psutil
from loguru import logger

from .config import Config
from .rep_mana import MeST

logger.remove(handler_id=None)
logger.add(
    os.path.expanduser("~/.cache/memest"),
    rotation="00:00",
    retention=datetime.timedelta(days=1),
    backtrace=True,
    diagnose=True,
    enqueue=True,
)
USAGE = """ USAGE memest [cmd]
cmd: start, status, stop, restart
"""

CONFIG_FILE = os.path.expanduser("~/.config/memest/config.ini")


def init_check():
    if not os.path.exists(CONFIG_FILE):
        print(f"please set `{CONFIG_FILE}`")
        exit(1)


def show_status():
    init_check()
    if is_memest_daemon_running():
        print("memest is running")
    else:
        print("memest is dead")
        return
    cfg = Config(CONFIG_FILE)
    all_rep = [i for i in cfg.get_sections() if i != "default"]
    print("sync:", all_rep)


def is_memest_daemon_running():
    for process in psutil.process_iter(["pid", "name", "cmdline"]):
        cmdline = " ".join(process.info["cmdline"])
        if "--daemon" in cmdline and "memest" in cmdline:
            return True
    return False


def stop_memest_daemon():
    for process in psutil.process_iter(["pid", "name", "cmdline"]):
        cmdline = " ".join(process.info["cmdline"])
        if "--daemon" in cmdline and "memest" in cmdline:
            os.kill(process.info["pid"], signal.SIGKILL)


def run_forever():
    cfg = Config(CONFIG_FILE)
    mestor = MeST(cfg)
    mestor.run()


def main():
    if len(sys.argv) < 2:
        print(USAGE)
        exit(1)
    cmd = sys.argv[1]
    os.system("mkdir -p ~/.cache/")
    init_check()
    if cmd == "start":
        if is_memest_daemon_running():
            print("memest is running")
        else:
            print("start memest")
            os.system("nohup memest --daemon >> /dev/null 2>&1 &")
    elif cmd == "status":
        show_status()
    elif cmd == "stop":
        stop_memest_daemon()
    elif cmd == "restart":
        os.system("memest stop")
        os.system("memest start")
    elif cmd == "--daemon":
        run_forever()
