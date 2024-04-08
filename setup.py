import os
import sys
import datetime
from setuptools import setup
from setuptools import find_packages


def get_today_date():
    today = datetime.date.today()
    return today.strftime("%Y.%m.%d")


VERSION = get_today_date().replace(".0", ".")

if sys.argv[1] == "publish":
    os.system("python3 setup.py sdist")
    os.system("python3 setup.py bdist_wheel")
    os.system("twine upload dist/*{}*".format(VERSION))
else:
    setup(
        name='MeMeST',
        version=VERSION,
        author='Xin-Xin Ma',
        description="Multi-Repository Sync Tool",
        description_content_type="text/markdown",
        long_description="auto-sync multi-repository",
        packages=find_packages(),
        data_files=[("", ["LICENSE"])],
        license="GPL",
        # project_urls={
            # 'Source': 'https://github.com/xxmawhu/LinuxRecycle',
        # },
        entry_points={'console_scripts': ['memest=mest.main:main']},
        install_requires=['termcolor', 'loguru', "psutil"]
    )
