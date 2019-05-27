#!/usr/bin/env python3

"""Setup script"""

from setuptools import setup, find_packages

setup(
    name="iotdev",
    description="IoT device framework",
    author="Michael Brown",
    author_email="mbrown@fensystems.co.uk",
    license="GPLv2+",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: "
        "GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python :: 3",
        "Topic :: Communications",
        "Topic :: Home Automation",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
    ],
    packages=find_packages(),
    install_requires=[
        'orderedset',
    ],
)
