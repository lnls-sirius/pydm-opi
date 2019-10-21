#!/usr/bin/env python3
from setuptools import setup, find_namespace_packages


with open('VERSION', 'r') as _f:
    __version__ = _f.read().strip()


with open('requirements.txt', 'r') as _f:
    _requirements = _f.read().strip().split('\n')


setup(
    name='siriushlacon',
    version=__version__,
    author='lnls-sirius',
    description='Client Applications for Sirius developed in PyDM by CONS',
    url='https://github.com/lnls-sirius/pydm-opi/',
    download_url='https://github.com/lnls-sirius/pydm-opi',
    license='GNU GPLv3',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering'
    ],
    install_requires=_requirements,
    packages=find_namespace_packages(include=['siriushlacon.*']),
    include_package_data=True,
    scripts=[
        'scripts/sirius-hla-as-ap-agilent4uhv.py',
        'scripts/sirius-hla-bo-ap-agilent4uhv-overview.py',
        'scripts/sirius-hla-si-ap-agilent4uhv-overview.py',
        'scripts/sirius-hla-as-ap-conlauncher.py',
        'scripts/sirius-hla-as-ap-pctrl.py',
        'scripts/sirius-hla-as-ap-mbtemp.py',
        'scripts/sirius-hla-as-ap-mks937b.py',
        'scripts/sirius-hla-bo-ap-mks937b-overview.py',
        'scripts/sirius-hla-si-ap-mks937b-overview.py',
        'scripts/sirius-hla-as-ap-regatron.py',
        'scripts/sirius-hla-as-ap-spixconv.py',
    ],
    zip_safe=False
)
