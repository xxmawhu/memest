#!/usr/bin/env python
# ====================================================
#   Copyright (C)2019 All rights reserved.
#
#   Author        : Xin-Xin MA
#   Email         : xxmawhu@163.com
#   File Name     : setup.py
#   Created Time  : 2019-09-24 10:51
#   Last Modified : 2019-09-29 12:09
#   Describe      :
#
# ====================================================

from setuptools import setup
from setuptools import find_packages
import sys
import os

m_version = '1.0.1'

if sys.argv[1] == "publish":
    os.system("python3 setup.py sdist")
    os.system("python3 setup.py bdist_wheel")
    os.system("twine upload dist/*{}*  --verbose".format(m_version))
else:
    setup(
        name='MeMeST',
        version=m_version,
        author='Xin-Xin Ma',
        description="Multi-Repository Sync Tool",
        description_content_type="text/markdown",
        long_description="auto-sync multi-repository",
        packages=find_packages(),
        data_files=[("", ["LICENSE"])],
        license="GPL",
        project_urls={
            'Source': 'https://github.com/xxmawhu/LinuxRecycle',
        },
        entry_points={'console_scripts': ['memest=mest.main:main']},
        install_requires=[
            'termcolor',
            'loguru',
        ]
    )
