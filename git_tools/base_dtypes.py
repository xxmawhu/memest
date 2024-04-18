import time
import hashlib


def unique_id(input_str):
    hash_object = hashlib.md5(input_str.encode())
    hex_dig = hash_object.hexdigest()
    unique_id = hex_dig[:12]
    return unique_id


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
        self.alias = unique_id(address)


class RepCacheData:
    local: RepData = None
    remote_rep_list = []

    def __init__(self, local, remote=[]):
        self.local = local
        self.remote_rep_list = remote
