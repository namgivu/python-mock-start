import os
from dotenv import load_dotenv

import unittest
from mockito import when, unstub


PWD = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=f'{PWD}/.env', override=False)
BEFORE_MOCKED_VAL = os.environ.get('SOME_VAR')


def tearDownModule():
    """
    whatever been mocked, here when test ends, the origin must stay working as normal
    """
    assert os.environ.get('SOME_VAR') is not None
    assert os.environ.get('SOME_VAR') == BEFORE_MOCKED_VAL


class Test(unittest.TestCase):

    def test_some_heavy_method__w_mockito(self):
        MOCKED_VAL = 'some mocked value here'

        # mock target code os.environ.get(:any)
        when(os.environ).get(Ellipsis).thenReturn(MOCKED_VAL)
        self.addCleanup(unstub)  # register mockito's unstub() method to unittest's cleanup

        ACT = os.environ.get('SOME_VAR')
        assert ACT == MOCKED_VAL
        assert ACT != BEFORE_MOCKED_VAL
