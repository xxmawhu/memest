import os
import subprocess
from loguru import logger
from .base_dtypes import RepData, RepCacheData


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_all_remotes(work_dir: str):
    cmd = ['git', 'remote', '-v']
    result = subprocess.check_output(cmd, cwd=work_dir, text=True).splitlines()
    remotes = [line.split('\t')[0] for line in result]
    return list(set(remotes))


def ensure_bare_repository(local_rep):
    address = local_rep.address
    if os.path.isdir(address) and os.path.isfile(os.path.join(address, 'config')):
        # logger.info("Address '{}' is already a bare Git repository.", local_rep.address)
        pass
    else:
        cmd = ['git', 'init', '--bare', local_rep.address]
        subprocess.run(cmd, check=True)


def init_rep(rep_data: RepData):
    mkdir(rep_data.work_dir)
    git_dir = os.path.join(rep_data.work_dir, '.git')
    is_git_repo = os.path.isdir(git_dir)
    if not is_git_repo:
        logger.info("Initializing {}", rep_data.work_dir)
        subprocess.run(['git', 'init'], cwd=rep_data.work_dir, check=False)
        logger.info("Repository {} initialized.", rep_data.work_dir)
    # 添加远程仓库
    if rep_data.alias == "":
        logger.error("[{}] alias is null", rep_data.address)
        return
    if rep_data.address == "":
        logger.error("address is null", rep_data.address)
        return
    if rep_data.alias == "local":
        ensure_bare_repository(rep_data)
    # 增加remote 仓库
    all_remotes = get_all_remotes(rep_data.work_dir)
    if rep_data.alias not in all_remotes:
        cmd = ['git', 'remote', 'add', rep_data.alias, rep_data.address]
        subprocess.run(cmd, cwd=rep_data.work_dir, check=False)


@logger.catch
def fetch(rep_data: RepData):
    if rep_data.key_file:
        key_file = rep_data.key_file
        cmd = ['ssh-agent', 'sh', '-c', f'GIT_SSH_COMMAND="ssh -i {key_file}" git fetch {rep_data.alias}']
    else:
        cmd = ['git', 'fetch', rep_data.alias]
    subprocess.run(cmd, cwd=rep_data.work_dir, check=True)


def update_branch_list(rep_data: RepData):
    pass


def push(rep_data: RepData):
    pass


def __merge_one_branch__(rep_data, local_branch):
    pass


def merge_all_branch(rep_data1, rep_data2):
    pass
