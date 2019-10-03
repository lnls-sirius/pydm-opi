#!/usr/bin/env python-sirius

from setuptools import setup, find_packages


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
    packages=find_packages(),
    package_data={
        'siriushlacon': [
            'VERSION', 'install.sh', 'launch.sh',
            'pydm-opi.desktop.template',
            'Redes e Beaglebones.xlsx',
            'agilent4uhv/ui/channel.ui',
            'agilent4uhv/ui/device_main.ui',
            'agilent4uhv/ui/device.ui',
            'agilent4uhv/ui/disp.ui',
            'agilent4uhv/ui/main.ui',
            'agilent4uhv/ui/run.sh',
            'launcher/ui/launcher.ui',
            'mbtemp/ui/main.ui',
            'mks937b/ui/booster.ui',
            'mks937b/ui/bts.ui',
            'mks937b/ui/cc.ui',
            'mks937b/ui/device_menu.ui',
            'mks937b/ui/device_preview.ui',
            'mks937b/ui/info.ui',
            'mks937b/ui/ioc_man.ui',
            'mks937b/ui/ltb.ui',
            'mks937b/ui/main.ui',
            'mks937b/ui/none.ui',
            'mks937b/ui/pirani.ui',
            'mks937b/ui/pressure.ui',
            'mks937b/ui/settings.ui',
            'mks937b/ui/storage_ring.ui',
            'mks937b/ui/table.ui',
            'tools/ui/archiver.ui',
            'tools/ui/bbb.ui',
            'utils/css/draw_no-invalid.qss',
            'utils/css/table-alarm.qss',
            'utils/images/booster.png',
            'utils/images/btts.png',
            'utils/images/CNPEM.jpg',
            'utils/images/dev.qrc',
            'utils/images/imgs.qrc',
            'utils/images/LNLS.png',
            'utils/images/ltb.png',
            'utils/images/ringB1A.png',
            'utils/images/ringB2A.png',
            'utils/images/storage_ring.png',
            'utils/images/vac.xcf',
            'utils/ui/overview.ui',
        ],
    },
    include_package_data=True,
    scripts=[
        'scripts/sirius-hla-as-ap-agilent4uhv.py',
        'scripts/sirius-hla-as-ap-conlauncher.py',
        'scripts/sirius-hla-as-ap-mbtemp.py',
        'scripts/sirius-hla-as-ap-mks937b.py',
        'scripts/sirius-hla-bo-ap-agilent4uhv-overview.py',
        'scripts/sirius-hla-bo-ap-mks937b-overview.py',
        'scripts/sirius-hla-si-ap-agilent4uhv-overview.py',
        'scripts/sirius-hla-si-ap-mks937b-overview.py',
    ],
    zip_safe=False
)
