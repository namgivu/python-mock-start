import os
from dotenv import load_dotenv

import unittest
from mockito import when, when2, unstub, patch

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

        # ACT2 = os.environ['SOME_VAR']  #NOTE this still NOT mocked and below :assert will fail --> solve it by test_mock__os_environ_dict()
        # assert ACT2 == MOCKED_VAL
        # assert ACT2 != BEFORE_MOCKED_VAL


    def TODOtest_mock__os_environ_dict(self):
        MOCKED_VAL = 'some mocked value @ SOME_VAR'
        MOCKED_DICT = {'SOME_VAR': MOCKED_VAL}

        # mock target code os.environ[:any]  #TODO asked on SO at https://stackoverflow.com/q/68030745/248616
        # when(os).environ[...].thenReturn(MOCKED_DICT)  #FIXME  #E       TypeError: 'StubbedInvocation' object is not subscriptable
        # when2(os.environ).thenReturn(MOCKED_DICT)      #FIXME  #E       AttributeError: 'function' object has no attribute 'get'
        # patch(os.environ, lambda str: MOCKED_DICT)     #FIXME  #E       AttributeError: 'function' object has no attribute 'get'
        # when(os.environ).__getitem__(...).thenReturn(MOCKED_VAL)  #FIXME this CANNOT get it mocked for environ[xx]  # mock environ[] by override bracket operator via __getitem__() ref. https://stackoverflow.com/a/1957793/248616
        self.addCleanup(unstub)  # register mockito's unstub() method to unittest's cleanup

        ACT_bybracket = os.environ['SOME_VAR']
        assert ACT_bybracket == MOCKED_DICT.get('SOME_VAR')
        assert ACT_bybracket != BEFORE_MOCKED_VAL


    def test_mock__patchdict(self):  # current working solution
        MOCKED_VAL = 'some mocked value @ SOME_VAR'
        MOCKED_DICT = {'SOME_VAR': MOCKED_VAL}

        from unittest.mock import patch ; p=patch.dict(in_dict=os.environ, values=MOCKED_DICT, clear=True) ; p.start()  # mock dict ref. ref. https://stackoverflow.com/a/44931447/248616
        self.addCleanup(p.stop)  # register mockito's unstub() method to unittest's cleanup

        ACT_bybracket = os.environ['SOME_VAR']
        assert ACT_bybracket == MOCKED_DICT.get('SOME_VAR')
        assert ACT_bybracket != BEFORE_MOCKED_VAL

        ACT_byget = os.environ.get('SOME_VAR')
        assert ACT_byget == MOCKED_DICT.get('SOME_VAR')
        assert ACT_byget != BEFORE_MOCKED_VAL
