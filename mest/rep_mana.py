import os
import time

from loguru import logger

import git_tools


def one_cycle_task(rep_data):
    git_tools.api.init_rep(rep_data)
    git_tools.api.fetch(rep_data)
    git_tools.api.merge_remote_branches(rep_data)
    git_tools.api.push(rep_data)


def sync_one_rep(rep):
    one_cycle_task(rep.local)
    for rep_data in rep.remote_rep_list:
        one_cycle_task(rep_data)


class MeST:
    rep_set = {}

    def __init__(self, cfg):
        self.cfg = cfg
        self.loop_period = self.cfg.get_intvalue("default.loop_period", 5)
        self.cache_dir = os.path.expanduser(self.cfg.get_value("default.cache"))

    def init_rep_set(self):
        all_rep = [i for i in self.cfg.get_sections() if i != "default"]
        logger.info("all_rep: {}", all_rep)
        for k in all_rep:
            local_data = git_tools.RepData(
                address=self.cfg.get_value(k + ".local"),
                work_dir=os.path.join(self.cache_dir, k),
            )
            remote_list = []
            for remote_cfg in self.cfg.get_list(k + ".remote", []):
                key_file = ""
                if "|" in remote_cfg:
                    key_file = remote_cfg.split("|")[1].strip()
                remote_data = git_tools.RepData(
                    address=self.cfg.get_value(remote_cfg.split("|")[0].strip()),
                    work_dir=os.path.join(self.cache_dir, k),
                    key_file=key_file,
                )
                remote_list.append(remote_data)
            rep = git_tools.RepCacheData(local=local_data, remote=remote_list)

    def check(self):
        if self.cfg.update_config():
            self.loop_period = self.cfg.get_intvalue("default.loop_period", 5)
            self.init_rep_set()

        for rep in self.rep_set.values():
            sync_one_rep(rep)

    def run(self):
        self.init_rep_set()
        while True:
            self.check()
            time.sleep(self.loop_period)
