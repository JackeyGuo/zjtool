#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 
# Copyright 2016 The TensorFlow Authors All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# @Time    : 2019/11/6 0006 7:16
# @Author  : peichao.xu
# @Email   : xj563853580@outlook.com
# @File    : setup.py
# @Usage   : python setup.py sdist bdist_wheel

# ==============================================================================

from __future__ import absolute_import, division, print_function

import os
import setuptools

try:
    # Override a non-pure "wheel" for pybind distributions
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel


    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False
except ImportError:
    bdist_wheel = None


def find_packages():
    def impl(root_dir, packages):
        filenames = os.listdir(root_dir)
        for filename in filenames:
            filepath = os.path.join(root_dir, filename)
            if os.path.isdir(filepath):
                impl(filepath, packages)
            else:
                if filename == '__init__.py':
                    packages.append(root_dir)

    packages = []
    impl('zjtool', packages)
    return packages


def find_package_data():
    binarys = ['cryption/encrypt', 'cryption/decrypt']
    return binarys


setuptools.setup(
    name='zjtool',
    version='0.1.4',
    author='peichao.xu',
    author_email="563853580@qq.com",
    url="https://github.com/afterimagex/zjtool.git",
    packages=find_packages(),
    license='BSD 2-Clause',
    install_requires=[
        'rich',
        'pymongo',
        'click',
        'requests',
        'pytest',
    ],
    package_data={'zjtool': find_package_data()},
    cmdclass={'bdist_wheel': bdist_wheel},
    entry_points={
        'console_scripts': [
            'zjtool = zjtool.main:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe=False,
)
