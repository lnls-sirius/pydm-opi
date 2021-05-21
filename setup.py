#!/usr/bin/env python3
import pkg_resources
from setuptools import find_packages, setup

from src.siriushlacon import __author__, __version__


def get_abs_path(relative) -> str:
    return pkg_resources.resource_filename(__name__, relative)


def get_long_description() -> str:
    desc = ""
    with open(get_abs_path("README.md"), "r") as _f:
        desc += _f.read().strip()

    desc += "\n\n"

    with open(get_abs_path("CHANGES.md"), "r") as _f:
        desc += _f.read().strip()

    return desc


long_description = get_long_description()

with open(get_abs_path("requirements.txt"), "r") as _f:
    requirements = _f.read().strip().split("\n")

setup(
    name="siriushlacon",
    author=__author__,
    classifiers=[
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
    ],
    description="Client Applications for Sirius",
    download_url="https://github.com/lnls-sirius/pydm-opi",
    license="GNU GPLv3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lnls-sirius/pydm-opi/",
    project_urls={
        "Changelog": "https://github.com/lnls-sirius/pydm-opi/",
    },
    version=__version__,
    install_requires=requirements,
    include_package_data=True,
    packages=find_packages(
        where="src",
        include=[
            "siriushlacon*",
        ],
    ),
    package_dir={"": "src"},
    python_requires=">=3.6",
    scripts=[
        "scripts/sirius-hla-as-ap-bbb-monitor.py",
        "scripts/sirius-hla-as-ap-conlauncher.py",
        "scripts/sirius-hla-as-ap-countingpru.py",
        "scripts/sirius-hla-as-ap-mbtemp.py",
        "scripts/sirius-hla-as-ap-pctrl.py",
        "scripts/sirius-hla-as-ps-regatron-individual.py",
        "scripts/sirius-hla-as-ps-regatron.py",
        "scripts/sirius-hla-as-pu-spixconv.py",
        "scripts/sirius-hla-as-va-agilent4uhv-device.py",
        "scripts/sirius-hla-as-va-agilent4uhv.py",
        "scripts/sirius-hla-as-va-mks937b.py",
        "scripts/sirius-hla-as-va-vbc.py",
        "scripts/sirius-hla-bo-va-agilent4uhv-overview.py",
        "scripts/sirius-hla-bo-va-mks937b-overview.py",
        "scripts/sirius-hla-si-va-agilent4uhv-overview.py",
        "scripts/sirius-hla-si-va-mks937b-overview.py",
        "scripts/sirius-hla-tb-va-agilent4uhv-overview.py",
        "scripts/sirius-hla-tb-va-mks937b-overview.py",
        "scripts/sirius-hla-ts-va-agilent4uhv-overview.py",
        "scripts/sirius-hla-ts-va-mks937b-overview.py",
    ],
    zip_safe=False,
)
