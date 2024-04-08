import time

from loguru import logger


class MeST:

    def __init__(self, cfg):
        self.cfg = cfg

    def check(self):
        if self.cfg.update_config():
            all_rep = [i for i in self.cfg.get_sections() if i != "default"]
            logger.info("all_rep: {}", all_rep)

    def run(self):
        while True:
            self.check()
            time.sleep(5)
