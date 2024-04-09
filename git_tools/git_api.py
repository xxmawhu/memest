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
    subprocess.run(cmd, cwd=rep_data.work_dir, check=True, stdout=subprocess.DEVNULL)
    update_branch_list(rep_data)


def get_remote_branches(work_dir, alias):
    """
    Given a local working directory (work_dir) and a remote alias (alias),
    return a list of all branches associated with the specified remote.

    Args:
        work_dir (str): Path to the local Git repository.
        alias (str): Name of the remote to fetch branches from.

    Returns:
        list[str]: List containing the names of all branches from the specified remote.
    """

    # Execute the 'git branch -r' command to list all remote branches

    # Run the command and capture its output

    # Filter the output to keep only the branches belonging to the given remote alias

    # Extract the branch names by removing the remote prefix (e.g., "alias/")


def update_branch_list(rep_data: RepData):
    work_dir = rep_data.work_dir
    git_command = ["git", "branch", "-r"]
    output = subprocess.check_output(git_command, text=True, cwd=work_dir)
    alias = rep_data.alias
    remote_branches = [line.strip() for line in output.splitlines() if line.strip().startswith(alias)]
    rep_data.branch_list = [branch_name[len(alias) + 1:] for branch_name in remote_branches]
    logger.info("remote_branches {}", rep_data.branch_list)


def get_local_branch_list(work_dir):
    git_command = ["git", "branch"]
    output = subprocess.check_output(git_command, text=True, cwd=work_dir)
    branch_list = [line.split(" ")[-1] for line in output.splitlines()]
    return branch_list


def push(rep_data: RepData):
    local_branch_list = get_local_branch_list(rep_data.work_dir)
    logger.info("[{}] local_branch_list:{}", rep_data.alias, local_branch_list)
    work_dir = rep_data.work_dir
    for branch in local_branch_list:
        checkout_command = ['git', 'checkout', branch]
        push_command = ['git', 'push', rep_data.alias, branch]
        logger.info("push:{}", " ".join(push_command))
        subprocess.run(checkout_command, cwd=work_dir, check=True, stdout=subprocess.DEVNULL)
        subprocess.run(push_command, cwd=work_dir, check=True, stdout=subprocess.DEVNULL)


def merge_remote_branches(rep_data):
    work_dir = rep_data.work_dir
    branch_list = rep_data.branch_list
    alias = rep_data.alias
    for branch in branch_list:
        checkout_command = ['git', 'checkout', branch]
        merge_command = ['git', 'merge', f'{alias}/{branch}']
        subprocess.run(checkout_command, cwd=work_dir, check=True, stdout=subprocess.DEVNULL)
        subprocess.run(merge_command, cwd=work_dir, check=True, stdout=subprocess.DEVNULL)


def __merge_one_branch__(rep_data, local_branch):
    pass


def merge_all_branch(rep_data1, rep_data2):
    pass
