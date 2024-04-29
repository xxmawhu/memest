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
LOG_FILE = os.path.expanduser("~/.cache/memest")
logger.add(
    LOG_FILE,
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


def get_log_error():
    error_lines = []
    for line in open(LOG_FILE, "r").read().splitlines():
        if "ERROR" in line:
            error_lines.append(line)
    content = "\n".join(error_lines[-10:])
    return content


def kill_process_tree(pid):
    sig = signal.SIGKILL
    pid_list = [pid]
    while True:
        if len(pid_list) == 0:
            break
        tmp_pid = pid_list.pop(0)
        if not psutil.pid_exists(tmp_pid):
            continue
        parent = psutil.Process(tmp_pid)
        if parent is not None:
            children = parent.children(recursive=False)
            if children is not None:
                for child in children:
                    pid_list.append(child.pid)
            cmdline = " ".join(parent.cmdline())
            print(f"kill {parent.pid} {cmdline}")
            parent.send_signal(sig)


def init_check():
    if not os.path.exists(CONFIG_FILE):
        print(f"please set `{CONFIG_FILE}`")
        exit(1)


def show_status():
    if is_memest_daemon_running():
        print("memest is running")
    else:
        print("memest is dead")
        return
    cfg = Config(CONFIG_FILE)
    all_rep = [i for i in cfg.get_sections() if i != "default"]
    print("sync:", all_rep)
    err_lines = get_log_error()
    if err_lines:
        print(err_lines)
        print(f"more details in {LOG_FILE}")


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
            pid = process.info["pid"]
            kill_process_tree(int(pid))


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
