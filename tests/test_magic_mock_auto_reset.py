import pytest, os
from unittest.mock import MagicMock


class TestMagicMockAutoReset:

    mocked_os = MagicMock()


    @pytest.mark.order1
    def test_step1_do_mocking(self):
        self.mocked_os.path.exists.return_value = 'mocked os.path.exists()'
        os = self.mocked_os
        assert os.path.exists('any path') == 'mocked os.path.exists()'


    @pytest.mark.order2 # :order2 will run after :order1
    def test_step2_check_mocked_method(self):
        assert os.path.exists('any path') is False # os.path.exists() here in :order2 test not be mocked after :order1 test has run
