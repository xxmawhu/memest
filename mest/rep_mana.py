import os
import time
from multiprocessing import Pool

from loguru import logger

import git_tools


@logger.catch
def one_cycle_task(rep_data):
    logger.info("fetch and merge for {}", rep_data.address)
    if not git_tools.api.init_rep(rep_data):
        return
    git_tools.api.fetch(rep_data)
    git_tools.api.merge_remote_branches(rep_data)
    git_tools.api.push(rep_data)


def sync_one_rep(rep_cache_data):
    git_tools.api.check_remotes(rep_cache_data)
    one_cycle_task(rep_cache_data.local)
    for rep_data in rep_cache_data.remote_rep_list:
        one_cycle_task(rep_data)


class MeST:
    rep_set = {}

    def __init__(self, cfg):
        self.cfg = cfg
        self.loop_period = self.cfg.get_intvalue("default.loop_period", 10)
        self.thread = self.cfg.get_intvalue("default.thread", 3)
        self.cache_dir = os.path.expanduser(self.cfg.get_value("default.cache"))
        git_tools.api.mkdir(self.cache_dir)

    def init_rep_set(self):
        all_rep = [i for i in self.cfg.get_sections() if i != "default"]
        logger.info("all_rep: {}", all_rep)
        self.rep_set = {}
        for k in all_rep:
            work_dir = os.path.join(self.cache_dir, k)
            address = os.path.expanduser(self.cfg.get_value(k + ".local"))
            local_data = git_tools.RepData(address=address, work_dir=work_dir)
            local_data.alias = "local"
            logger.info("local_data:\n{}", local_data)
            remote_list = []
            for remote_cfg in self.cfg.get_list(k + ".remote", []):
                address = remote_cfg.split("|")[0].strip()
                key_file = ""
                if "|" in remote_cfg:
                    key_file = os.path.expanduser(remote_cfg.split("|")[1].strip())
                remote_data = git_tools.RepData(
                    address=address, work_dir=work_dir, key_file=key_file
                )
                remote_list.append(remote_data)
                logger.info("add:\n{}", remote_data)
            self.rep_set[k] = git_tools.RepCacheData(
                local=local_data, remote=remote_list
            )
            git_tools.api.check_remotes(self.rep_set[k])

    def check(self):
        if self.cfg.update_config():
            self.loop_period = self.cfg.get_intvalue("default.loop_period", 5)
            self.init_rep_set()

        # for rep in self.rep_set.values():
        # sync_one_rep(rep)
        with Pool(self.thread) as p:
            p.map(sync_one_rep, self.rep_set.values())

    def run(self):
        self.init_rep_set()
        while True:
            try:
                self.check()
            except Exception as e:
                logger.error("{}", e)
            time.sleep(int(self.loop_period))
