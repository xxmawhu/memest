import os
import sys
import glob
import signal
import datetime
import subprocess

import psutil
from loguru import logger

from .config import Config
from .rep_mana import MeST

logger.remove(handler_id=None)
LOG_FILE = os.path.expanduser("~/.cache/mmst/memest") + ".{time:YYYYMMDD}"
logger.add(
    LOG_FILE,
    rotation="00:00",
    retention=datetime.timedelta(days=5),
    backtrace=True,
    diagnose=True,
    enqueue=True,
)
USAGE = """ USAGE memest [cmd]
cmd: start, status, stop, restart
"""

CONFIG_FILE = os.path.expanduser("~/.config/memest/config.ini")


def add_cron_job_if_not_exists(cron_command, schedule):
    tmp_crontab_file = "tmp_my_crontab"
    subprocess.run(["crontab", "-l"], stdout=open(tmp_crontab_file, "w"), check=True)
    all_tasks = open(tmp_crontab_file, "r").read()
    cmd = f"{schedule} {cron_command}"
    if cmd in all_tasks:
        subprocess.run(["rm", "-f", tmp_crontab_file], check=False)
        return

    with open(tmp_crontab_file, "a") as file:
        file.write(f"{schedule} {cron_command}\n")
    subprocess.run(["crontab", tmp_crontab_file], check=False)
    subprocess.run(["rm", "-f", tmp_crontab_file], check=False)


def get_log_error():
    error_lines = []
    log_file = sorted(glob.glob(os.path.expanduser("~/.cache/mmst/memest.*")))[-1]
    for line in open(log_file, "r").read().splitlines():
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
        try:
            tmp_pid = pid_list.pop(0)
            if not psutil.pid_exists(tmp_pid):
                continue
            parent = psutil.Process(tmp_pid)
            if parent is not None:
                children = parent.children(recursive=False)
                if children is not None:
                    for child in children:
                        pid_list.append(child.pid)
                if parent.cmdline is not None:
                    cmdline = " ".join(parent.cmdline())
                    print(f"kill {parent.pid} {cmdline}")
                parent.send_signal(sig)
        except Exception as e:
            print(e)


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
        if process.info["cmdline"] is None:
            continue
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
        add_cron_job_if_not_exists("memest start", "@reboot")
        add_cron_job_if_not_exists("memest start", "@daily")
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
