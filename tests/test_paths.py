import inspect
import os
import unittest

import siriushlacon.agilent4uhv.consts as agilent_consts
import siriushlacon.beaglebones.consts as beagle_consts
import siriushlacon.countingpru.consts as counting_pru_consts
import siriushlacon.danfysik.consts as danfysik_consts
import siriushlacon.mbtemp.consts as mbtemp_consts
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
        return [getattr(module, attr) for attr in attrs]

    def _check_get_abs_path_of_module(self, module):
        for f in self._get_paths_from_module(module):
            self.assertTrue(os.path.exists(f), f"Check '{f}' exists")

    def test_conting_pru(self):
        self._check_get_abs_path_of_module(counting_pru_consts)

    def test_beagle(self):
        for f in [
            beagle_consts.BEAGLEBONES_MAIN,
            beagle_consts.BEAGLEBONES_MAIN_UI,
            beagle_consts.INFO_BBB_UI,
            beagle_consts.CHANGE_BBB_UI,
            beagle_consts.LOGS_BBB_UI,
            beagle_consts.RED_LED,
            beagle_consts.GREEN_LED,
        ]:
            self.assertTrue(os.path.exists(f))

    def test_mks(self):
        for f in [
            mbtemp_consts.MBTEMP_MAIN,
            mbtemp_consts.MBTEMP_MAIN_UI,
            mbtemp_consts.OVERVIEW_MAIN,
            mbtemp_consts.OVERVIEW_MAIN_UI,
            mbtemp_consts.BOEXTRACTION_PIC,
            mbtemp_consts.BOINJ_PIC,
            mbtemp_consts.BO_PIC1,
            mbtemp_consts.BO_PIC2,
            mbtemp_consts.BO_PIC3,
            mbtemp_consts.BO_PIC4,
            mbtemp_consts.CNPEM_LOGO,
            mbtemp_consts.LNLS_LOGO,
            mbtemp_consts.SRINJ_PIC,
            mbtemp_consts.SR_PIC1,
            mbtemp_consts.SR_PIC2,
            mbtemp_consts.SR_PIC3,
            mbtemp_consts.SR_PIC4,
            mbtemp_consts.SR_PIC5,
            mbtemp_consts.SR_PIC6,
            mbtemp_consts.SR_PIC7,
            mbtemp_consts.PIC_PA,
            mbtemp_consts.PIC_LA,
            mbtemp_consts.PIC_P7RF,
        ]:
            self.assertTrue(os.path.exists(f))

    def test_regatron(self):
        for f in [
            regatron_consts.DATA_JSON,
            regatron_consts.REGATRON_MAIN,
            regatron_consts.TREE_32,
            regatron_consts.COMPLETE_MAIN,
            regatron_consts.ALARM_MAIN,
            regatron_consts.REGATRON_UI,
            regatron_consts.TREE_32_UI,
            regatron_consts.COMPLETE_UI,
            regatron_consts.ALARM_UI,
            regatron_consts.ERROR_LIST_PDF,
        ]:
            self.assertTrue(os.path.exists(f))

    def test_spixconv(self):
        for f in [spixconv_consts.SPIXCONV_MAIN]:
            self.assertTrue(os.path.exists(f))

    def test_agilent(self):
        for f in [
            agilent_consts.AGILENT_CHANNEL,
            agilent_consts.AGILENT_CHANNEL_UI,
            agilent_consts.AGILENT_DEVICE,
            agilent_consts.AGILENT_DEVICE_MAIN,
            agilent_consts.AGILENT_DEVICE_MAIN_UI,
            agilent_consts.AGILENT_DEVICE_UI,
            agilent_consts.AGILENT_EXTENDED,
            agilent_consts.AGILENT_MAIN,
            agilent_consts.AGILENT_MAIN_UI,
            agilent_consts.AGILENT_OVERVIEW,
        ]:
            self.assertTrue(os.path.exists(f))

    def test_danfysik(self):
        self.assertTrue(os.path.exists(danfysik_consts.DANSYFIK_MAIN_PY))
        self.assertTrue(os.path.exists(danfysik_consts.DANSYFIK_MAIN_UI))

    def test_vbc(self):
        for f in [
            vbc_consts.CHECK_IMG,
            vbc_consts.CNPEM_IMG,
            vbc_consts.LNLS_IMG,
            vbc_consts.PLAY_IMG,
            vbc_consts.STOP_IMG,
            vbc_consts.WARNING_IMG,
            vbc_consts.ADVANCED_WINDOW_UI,
            vbc_consts.CONFIRMATION_MESSAGE_UI,
            vbc_consts.MAIN_WINDOW_UI,
            vbc_consts.OK_MESSAGE_UI,
            vbc_consts.SYSTEM_WINDOW_UI,
            vbc_consts.WARNING_WINDOW_UI,
            vbc_consts.SIMPLE_WINDOW_UI,
            vbc_consts.ADVANCED_WINDOW_PY,
            vbc_consts.CONFIRMATION_MESSAGE_PY,
            vbc_consts.MAIN_WINDOW_PY,
            vbc_consts.OK_MESSAGE_PY,
            vbc_consts.SYSTEM_WINDOW_PY,
            vbc_consts.WARNING_WINDOW_PY,
            vbc_consts.SIMPLE_WINDOW_PY,
        ]:
            self.assertTrue(os.path.exists(f))
