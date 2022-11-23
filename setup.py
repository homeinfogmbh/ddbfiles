#! /usr/bin/env python3

from setuptools import setup

setup(
    name='ddbfiles',
    use_scm_version={
        "local_scheme": "node-and-timestamp"
    },
    setup_requires=['setuptools_scm'],
    install_requires=[
        'configlib',
        'emaillib',
        'flask',
        'his',
        'setuptools',
        'wsgilib'
    ],
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='<info at homeinfo dot de>',
    maintainer='Richard Neumann',
    maintainer_email='<r dot neumann at homeinfo priod de>',
    packages=['ddbfiles'],
    entry_points={
        'console_scripts': [
            'ddbfiles-notify = ddbfiles.notifications:main'
        ]
    },
    data_files=[
        ('/usr/lib/systemd/system', [
            'files/ddbfiles-watchdog.service'
        ])
    ],
    scripts=[
        'files/ddbfiles-watchdog'
    ],
    license='GPLv3',
    description='Authorized download for DDB related files.'
)
