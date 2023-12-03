# Copyright (c) 2018 Cloudify Platform Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
import sys
import pathlib
from setuptools import setup, find_packages


def get_version():
    current_dir = pathlib.Path(__file__).parent.resolve()
    with open(os.path.join(current_dir,'cloudify_spot_ocean/__version__.py'),
              'r') as outfile:
        var = outfile.read()
        return re.search(r'\d+.\d+.\d+', var).group()


install_requires = [
        'pycryptodome==3.9.7',
        'requests>=2.25.0,<3.0.0',
        'spotinst_sdk2',
        'botocore',
        'boto3'
]
if sys.version_info.major == 3 and sys.version_info.minor == 6:
    packages = ['cloudify_spot_ocean', 'spot_ocean_sdk']
    install_requires += [
        'deepdiff==3.3.0',
        'cloudify-common>=5.1.0,<7.0',
        'cloudify-utilities-plugins-sdk>=0.0.127',
    ]
else:
    packages = find_packages()
    install_requires += [
        'deepdiff==5.7.0',
        'fusion-common',
        'cloudify-utilities-plugins-sdk',
    ]


setup(
    name='cloudify-spot-ocean-plugin',
    version=get_version(),
    author='Cloudify Platform Ltd.',
    author_email='hello@cloudify.co',
    license='LICENSE',
    packages=packages,
    description='A Cloudify plugin for Spot Ocean',
    install_requires=install_requires
)
