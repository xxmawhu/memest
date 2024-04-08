class RepData:
    update_time = 0
    timeout = 600
    alias = ""
    address = None
    work_dir = ""
    key_file = ""
    branch_list = []


class RepCacheData:
    local = RepData()
    remote_rep_list = []
