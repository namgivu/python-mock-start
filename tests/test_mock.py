import unittest
from unittest.mock  import patch, MagicMock  # ref. https://docs.python.org/3/library/unittest.mock.html#quick-guide
from mockito        import when, unstub

from services import some_service


def setUpModule(): pass  # nothing here for now

def tearDownModule():
    """
    whatever been mocked, here when it ends, the method should return to its original code
    we prove it here
    """
    a=1; b=22
    r = some_service.some_heavy_method(a, b)
    assert r == a + b == 23


class Test(unittest.TestCase):

    def setUp(self):    pass  # nothing here for now
    def tearDown(self): pass  # nothing here for now


    def test_some_heavy_method__no_mock(self):
        a=1; b=22
        r = some_service.some_heavy_method(a, b)
        assert r == a+b == 23


    #region test_some_heavy_method__w_builtin
    """All feasible techniques to do mocking with the builtin"""

    '''use decorator'''
    @patch('services.some_service.some_heavy_method', MagicMock(return_value=4444))  # mocking some_heavy_method() to return 4444
    def test_some_heavy_method__w_builtin1a(self):
        a=1; b=22
        r = some_service.some_heavy_method(a, b)
        assert r == 4444 != a+b == 23
        # NOTE the @patch() has auto-reset mocked method to its original code


    '''decorator with value set from mock object'''
    m = MagicMock(); m.return_value = 55555
    @patch('services.some_service.some_heavy_method', m)
    def test_some_heavy_method__w_builtin1b(self):
        a=1; b=22; r = some_service.some_heavy_method(a, b)
        assert r == 55555 != a+b == 23
        # NOTE the @patch() has auto-reset mocked method to its original code


    #region built-in mock without decorator
    '''no decorator patch - directly using MagicMock object'''
    def test_some_heavy_method__w_builtin2a(self):
        _origin_code = some_service.some_heavy_method  # save origin code before mocking
        def unpatch(): some_service.some_heavy_method = _origin_code
        self.addCleanup(unpatch)  # reset mocked method to its original code

        # do mocking
        m = MagicMock(); m.return_value = 677888; some_service.some_heavy_method = m

        # check mocked method outcome
        a=1; b=22; r = some_service.some_heavy_method(a, b)
        assert r == 677888 != a+b == 23


    '''no decorator patch - directly using patch object'''
    def test_some_heavy_method__w_builtin2b(self):
        pt = patch('services.some_service.some_heavy_method', MagicMock(return_value=677888)); pt.start(); self.addCleanup(pt.stop)
        # NOTE the pt.stop() will auto-reset mocked method to its original code

        # check mocked method outcome
        a=1; b=22; r = some_service.some_heavy_method(a, b)
        assert r == 677888 != a+b == 23

    #endregion built-in mock without decorator

    #endregion


    """With the game-changer mockito, things get a lot simpler"""
    def test_some_heavy_method__w_mockito(self):
        when(some_service).some_heavy_method(Ellipsis, Ellipsis).thenReturn(333)
        self.addCleanup(unstub)  # reset mocked method to its original code

        a=1; b=22
        r = some_service.some_heavy_method(a, b)
        assert r == 333 != a+b == 23
