import inspect
import os
import unittest

import siriushlacon.agilent4uhv.consts as agilent_consts
import siriushlacon.beaglebones.consts as beagle_consts
import siriushlacon.countingpru.consts as counting_pru_consts
import siriushlacon.danfysik.consts as danfysik_consts
import siriushlacon.epicstel.consts as tel_consts
import siriushlacon.mbtemp.consts as mbtemp_consts
import siriushlacon.mks937b.consts as mks_consts
import siriushlacon.pctrl.consts as pctrl_consts
import siriushlacon.regatron.consts as regatron_consts
import siriushlacon.spixconv.consts as spixconv_consts
import siriushlacon.vbc.consts as vbc_consts


class ConstsFileReference(unittest.TestCase):
    def _get_paths_from_module(self, module):
        attrs = [
            i.split(" = ")[0]
            for i in inspect.getsource(module).split("\n")
            if i.strip() and " = get_abs_path" in i
        ]
        return [(attr, getattr(module, attr)) for attr in attrs]

    def _check_get_abs_path_of_module(self, module):
        for key, value in self._get_paths_from_module(module):
            self.assertTrue(os.path.exists(value), f"Check '{key} = {value!r}' exists")

    def test_pctrl(self):
        self._check_get_abs_path_of_module(pctrl_consts)

    def test_epics_tel(self):
        self._check_get_abs_path_of_module(tel_consts)

    def test_conting_mks(self):
        self._check_get_abs_path_of_module(mks_consts)

    def test_conting_pru(self):
        self._check_get_abs_path_of_module(counting_pru_consts)

    def test_beagle(self):
        self._check_get_abs_path_of_module(beagle_consts)

    def test_mbtemp(self):
        self._check_get_abs_path_of_module(mbtemp_consts)

    def test_regatron(self):
        self._check_get_abs_path_of_module(regatron_consts)

    def test_spixconv(self):
        self._check_get_abs_path_of_module(spixconv_consts)

    def test_agilent(self):
        self._check_get_abs_path_of_module(agilent_consts)

    def test_danfysik(self):
        self._check_get_abs_path_of_module(danfysik_consts)

    def test_vbc(self):
        self._check_get_abs_path_of_module(vbc_consts)
