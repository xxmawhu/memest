import git_tools

data = git_tools.RepData(
    # address="git@codeup.aliyun.com:xxmawhu/example.git",
    address="git@codeup.aliyun.com:625991e0594c6cca64842e0d/xxmawhu/example.git",
    work_dir="/home/maxx/.local/git_cache/example"
)

print(data)
exit(0)
data = git_tools.RepData(
    address="git@github.com:xxmawhu/example.git", work_dir="/home/maxx/.local/git_cache/example"
)

git_tools.api.init_rep(data)
git_tools.api.fetch(data)
