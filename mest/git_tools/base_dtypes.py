import time


class RepData:
    update_time = 0
    timeout = 600
    alias = ""
    address = None
    work_dir = ""
    key_file = ""
    branch_list = []

    def __str__(self):
        s = "address:" + self.address + "\n"
        s += f"alias:{self.alias}\n"
        s += f"work_dir:{self.work_dir}\n"
        s += f"key_file:{self.key_file}\n"
        s += f"branch_list:{self.branch_list}\n"
        return s

    def __init__(self, address, work_dir, key_file="", timeout=None):
        """
        @address git@github.com:xxmawhu/example.git
        """
        self.update_time = time.time()
        self.address = address
        self.work_dir = work_dir
        self.key_file = key_file
        self.timeout = timeout or 600
        if ".com" in address:
            usr = "_".join(address.split(":")[-1].split("/")[:]).replace(".git", "")
            host = address.split("@")[-1].split(".")[0]
            self.alias = f"{host}_{usr}"
        else:
            self.alias = "local"


class RepCacheData:
    local: RepData = None
    remote_rep_list = []
