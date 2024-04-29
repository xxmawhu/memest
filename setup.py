import os
import sys
import datetime
import subprocess
from setuptools import setup
from setuptools import find_packages


def get_latest_commit_hash():
    try:
        # 使用git log命令获取最新一次提交的SHA-1值，-n 1表示只获取最近的一条提交记录
        # --pretty=format:%H指定了输出格式，只输出commit的SHA-1值
        output = subprocess.check_output(
            ["git", "log", "-n", "1", "--pretty=format:%H"]
        )
        # 将输出的字节串转换为字符串，并去掉末尾的换行符
        commit_hash = output.decode("utf-8").strip()
        return commit_hash
    except subprocess.CalledProcessError as e:
        return None
    except FileNotFoundError:
        return None


def get_today_date():
    today = datetime.datetime.now()
    return today.strftime("%Y.%m.%d")


VERSION = get_today_date().replace(".0", ".")

HASH = get_latest_commit_hash()
if HASH is None:
    exit(1)
VERSION += "." + HASH[:6]

if sys.argv[1] == "publish":
    os.system("rm -rf dist/")
    os.system("python3 setup.py bdist_wheel")
    os.system("twine upload dist/*")
else:
    setup(
        name="MeMeST",
        version=VERSION,
        author="Xin-Xin Ma",
        description="Multi-Repository Sync Tool",
        description_content_type="text/markdown",
        long_description_content_type="text/markdown",
        long_description=open("./Readme.md", "r").read(),
        packages=find_packages(),
        data_files=[("", ["LICENSE"])],
        license="GPL",
        project_urls={
            "Source": "https://github.com/xxmawhu/memest.git",
        },
        entry_points={"console_scripts": ["memest=mest.main:main"]},
        install_requires=["termcolor", "loguru", "psutil"],
    )
