import pytest
from unittest.mock import MagicMock


class SomeClass:

    @staticmethod
    def some_method():
        return 'some_method returned value'


mocked_obj = MagicMock()
stash = None


class TestMagicMockAutoReset:


    def test_step0_check_mocked_method(self):
        print(1)
        assert SomeClass.some_method() == 'some_method returned value'


    def test_step1_do_mocking(self):
        print(2)
        # save before mock to :stash
        global stash; stash = SomeClass.some_method

        # do mock
        mocked_obj.return_value = 'mocked'
        SomeClass.some_method = mocked_obj

        # check mocked value
        assert SomeClass.some_method() == 'mocked'


    def test_step3_check_mocked_method(self):
        print(3)

        assert SomeClass.some_method() == 'mocked' # mocked value in :2 still being kept here

        mocked_obj.reset_mock()
        assert SomeClass.some_method() == 'mocked' # .reset_mock() not recover the mocked method to its original code


        global stash; SomeClass.some_method = stash # restore from the :stash
        assert SomeClass.some_method() == 'some_method returned value' # only after reset, original return comes back

        assert SomeClass.some_method() == 'some_method returned value'
