import os
import unittest

from siriushlacon.danfysik.consts import DANSYFIK_MAIN_PY, DANSYFIK_MAIN_UI


class DanfisykStaticFiles(unittest.TestCase):
    def test_file_exist(self):
        self.assertTrue(os.path.exists(DANSYFIK_MAIN_PY))
        self.assertTrue(os.path.exists(DANSYFIK_MAIN_UI))
