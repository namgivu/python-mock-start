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

    def test_mock__os_environ_get(self):
        MOCKED_VAL = 'some mocked value here @ test_mock__os_environ_get'

        # mock target code os.environ.get(:any)
        when(os.environ).get(...).thenReturn(MOCKED_VAL)
        self.addCleanup(unstub)  # register mockito's unstub() method to unittest's cleanup

        ACT = os.environ.get('SOME_VAR')
        assert ACT == MOCKED_VAL
        assert ACT != BEFORE_MOCKED_VAL


    def TODOtest_mock__os_environ_dict(self):
        MOCKED_VAL = 'some mocked value here @ test_mock__os_environ_dict'

        # mock target code os.environ[:any]
        when(os).environ[...].thenReturn(MOCKED_VAL)  #ERROR TypeError: 'StubbedInvocation' object is not subscriptable
        self.addCleanup(unstub)  # register mockito's unstub() method to unittest's cleanup

        ACT = os.environ.get('SOME_VAR')
        assert ACT == MOCKED_VAL
        assert ACT != BEFORE_MOCKED_VAL
