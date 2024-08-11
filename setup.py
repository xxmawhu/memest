import os
import sys
import subprocess
from setuptools import setup
from setuptools import find_packages


def get_version():
    try:
        output = (
            subprocess.check_output(
                ["git", "log", "--pretty=format:%ad %H", "--date=short"]
            )
            .decode()
            .splitlines()
        )
    except subprocess.CalledProcessError as e:
        print("Error executing git log:", e)
        return None
    main_version = output[0][:7]
    sub_version = len([i for i in output if i.startswith(main_version)])
    year, month = main_version.split("-")
    return f"{year}.{int(month)}.{sub_version}"


VERSION = get_version()

if sys.argv[1] == "publish":
    print("version:", VERSION)
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
