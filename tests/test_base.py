import unittest

import pytest
from requests.exceptions import HTTPError

from tests import genius

pytestmark = pytest.mark.skip(reason="This test is under development.")


class TestAPIBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n---------------------\nSetting up API base tests...\n")

    def test_http_error_handler(self):
        status_code = None
        try:
            genius.annotation(0)
        except HTTPError as e:
            status_code = e.args[0]

        self.assertEqual(status_code, 404)
