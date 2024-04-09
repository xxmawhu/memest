import git_tools

aliyun_data = git_tools.RepData(
    address="git@codeup.aliyun.com:625991e0594c6cca64842e0d/xxmawhu/example.git",
    work_dir="/home/maxx/.local/git_cache/example"
)
local_data = git_tools.RepData(
    address="/home/maxx/.local/git_cache/example.git",
    work_dir="/home/maxx/.local/git_cache/example",
)
print(local_data)

github_data = git_tools.RepData(
    address="git@github.com:xxmawhu/example.git",
    work_dir="/home/maxx/.local/git_cache/example",
)
rep_set = git_tools.RepCacheData(local=local_data, remote=[aliyun_data, github_data])
