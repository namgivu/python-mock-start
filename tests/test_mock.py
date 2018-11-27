import unittest

from services import some_service


def setUpModule():    pass # nothing here for now
def tearDownModule(): pass # nothing here for now


class Test00(unittest.TestCase):

    def setUp(self):    pass # nothing here for now
    def tearDown(self): pass # nothing here for now


    def test_some_heavy_method__no_mock(self):
        a=1; b=22
        r = some_service.some_heavy_method(a, b)
        assert r == a+b == 23


    def test_some_heavy_method__w_mockito(self):
        from mockito import when
        when(some_service).some_heavy_method(Ellipsis, Ellipsis).thenReturn(333)

        a=1; b=22
        r = some_service.some_heavy_method(a, b)
        assert r == 333 != a+b == 23


    #region test_some_heavy_method__w_builtin
    from unittest.mock import patch, MagicMock # ref. https://docs.python.org/3/library/unittest.mock.html#quick-guide

    @patch('services.some_service.some_heavy_method', MagicMock(return_value=4444)) # mocking some_heavy_method() to return 4444
    def test_some_heavy_method__w_builtin1(self):
        a=1; b=22
        r = some_service.some_heavy_method(a, b)
        assert r == 4444 != a+b == 23


    mocked_some_heavy_method = MagicMock()
    mocked_some_heavy_method.return_value = 55555

    @patch('services.some_service.some_heavy_method', mocked_some_heavy_method)
    def test_some_heavy_method__w_builtin2(self):
        a=1; b=22
        r = some_service.some_heavy_method(a, b)
        assert r == 55555 != a+b == 23
    #endregion
