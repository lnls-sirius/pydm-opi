#!/usr/bin/env python3
from setuptools import setup, find_namespace_packages


with open("VERSION", "r") as _f:
    __version__ = _f.read().strip()


with open("requirements_sirius.txt", "r") as _f:
    _requirements = _f.read().strip().split("\n")


setup(
    name="siriushlacon",
    version=__version__,
    author="lnls-sirius",
    description="Client Applications for Sirius developed in PyDM by CONS",
    url="https://github.com/lnls-sirius/pydm-opi/",
    download_url="https://github.com/lnls-sirius/pydm-opi",
    license="GNU GPLv3",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
    ],
    install_requires=_requirements,
    packages=find_namespace_packages(include=["siriushlacon", "siriushlacon.*"]),
    include_package_data=True,
    scripts=[
        "scripts/sirius-hla-as-va-agilent4uhv.py",
        "scripts/sirius-hla-as-va-agilent4uhv-device.py",
        "scripts/sirius-hla-tb-va-agilent4uhv-overview.py",
        "scripts/sirius-hla-bo-va-agilent4uhv-overview.py",
        "scripts/sirius-hla-ts-va-agilent4uhv-overview.py",
        "scripts/sirius-hla-si-va-agilent4uhv-overview.py",
        "scripts/sirius-hla-as-ap-bbb-monitor.py",
        "scripts/sirius-hla-as-ap-conlauncher.py",
        "scripts/sirius-hla-as-ap-countingpru.py",
        "scripts/sirius-hla-as-ap-mbtemp.py",
        "scripts/sirius-hla-as-va-mks937b.py",
        "scripts/sirius-hla-tb-va-mks937b-overview.py",
        "scripts/sirius-hla-bo-va-mks937b-overview.py",
        "scripts/sirius-hla-ts-va-mks937b-overview.py",
        "scripts/sirius-hla-si-va-mks937b-overview.py",
        "scripts/sirius-hla-as-ps-regatron.py",
        "scripts/sirius-hla-as-ps-regatron-individual.py",
        "scripts/sirius-hla-as-pu-spixconv.py",
    ],
    zip_safe=False,
)
