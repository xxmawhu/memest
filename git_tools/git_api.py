import os
import subprocess
from loguru import logger
from .base_dtypes import RepData, RepCacheData

ENV = os.environ.copy()
ENV["LD_LIBRARY_PATH"] = ""
ENV["PATH"] = "/usr/bin:/bin:/usr/local/bin"
del ENV["OPENSSL_DIR"]
print(ENV)


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_all_remotes(work_dir: str):
    cmd = ["git", "remote", "-v"]
    result = subprocess.check_output(
        cmd,
        cwd=work_dir,
        text=True,
        env=ENV,
    ).splitlines()
    remotes = [line.split("\t")[0] for line in result]
    return list(set(remotes))


def get_local_branch_list(work_dir):
    git_command = ["git", "branch"]
    output = subprocess.check_output(git_command, text=True, cwd=work_dir)
    branch_list = [line.split(" ")[-1] for line in output.splitlines()]
    return branch_list


def good_rep_data(rep_data):
    return rep_data.alias and rep_data.address and rep_data.work_dir


def ensure_bare_repository(rep_data):
    if not good_rep_data(rep_data):
        return
    address = rep_data.address
    if os.path.isdir(address) and os.path.isfile(os.path.join(address, "config")):
        # logger.info("Address '{}' is already a bare Git repository.", local_rep.address)
        pass
    else:
        cmd = ["git", "init", "--bare", rep_data.address]
        subprocess.run(cmd, check=True)
        logger.info("init bare repository:{}", rep_data.address)


def init_rep(rep_data: RepData):
    if not good_rep_data(rep_data):
        return
    mkdir(rep_data.work_dir)
    # logger.info("{}: init_rep", rep_data.address)
    git_dir = os.path.join(rep_data.work_dir, ".git")
    is_git_repo = os.path.isdir(git_dir)
    if not is_git_repo:
        logger.info("Initializing {}", rep_data.work_dir)
        subprocess.run(["git", "init"], cwd=rep_data.work_dir, check=False, text=True)
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
        logger.info("{} as remote", rep_data.address)
        cmd = ["git", "remote", "add", rep_data.alias, rep_data.address]
        subprocess.run(cmd, cwd=rep_data.work_dir, check=True)


@logger.catch
def fetch(rep_data: RepData):
    if not good_rep_data(rep_data):
        return
    logger.info("fetch {}", rep_data.address)
    cmd = []
    if rep_data.key_file:
        git_ssh_command = f'ssh -i "{rep_data.key_file}"'
        cmd.append(git_ssh_command)
    cmd += ["git", "fetch", rep_data.alias]
    result = subprocess.run(
        cmd,
        env=ENV,
        cwd=rep_data.work_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        logger.error(
            "fetch {} fail, code:{} reason:{}",
            rep_data.address,
            result.returncode,
            result.stderr.decode("utf-8"),
        )
        return
    update_branch_list(rep_data)


def update_branch_list(rep_data: RepData):
    work_dir = rep_data.work_dir
    git_command = ["git", "branch", "-r"]
    output = subprocess.check_output(git_command, text=True, cwd=work_dir)
    alias = rep_data.alias
    remote_branches = [line.strip() for line in output.splitlines() if line.strip().startswith(alias)]
    rep_data.branch_list = [branch_name[len(alias) + 1:] for branch_name in remote_branches]
    # logger.info("remote_branches {}", rep_data.branch_list)


@logger.catch
def push(rep_data: RepData):
    if not good_rep_data(rep_data):
        return
    local_branch_list = get_local_branch_list(rep_data.work_dir)
    logger.info("push to {}", rep_data.address)
    work_dir = rep_data.work_dir
    for branch in local_branch_list:
        checkout_command = ["git", "checkout", branch]
        subprocess.run(
            checkout_command,
            cwd=work_dir,
            check=True,
            stdout=subprocess.DEVNULL,
        )
        push_command = []
        if rep_data.key_file:
            git_ssh_command = f'ssh -i "{rep_data.key_file}"'
            push_command.append(git_ssh_command)

        push_command += ["git", "push", rep_data.alias, branch]
        result = subprocess.run(
            push_command,
            cwd=work_dir,
            env=ENV,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode != 0:
            logger.error(
                "pus to {} fail, code:{} reason:{}",
                rep_data.address,
                result.returncode,
                result.stderr.decode("utf-8"),
            )


def merge_remote_branches(rep_data):
    if not good_rep_data(rep_data):
        return
    work_dir = rep_data.work_dir
    branch_list = rep_data.branch_list
    alias = rep_data.alias
    for branch in branch_list:
        checkout_command = ["git", "checkout", branch]
        merge_command = ["git", "merge", f"{alias}/{branch}"]
        subprocess.run(checkout_command, cwd=work_dir, check=True, stdout=subprocess.DEVNULL)
        subprocess.run(merge_command, cwd=work_dir, check=True, stdout=subprocess.DEVNULL)
