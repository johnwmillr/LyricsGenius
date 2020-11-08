import unittest

from requests.exceptions import HTTPError

try:
    from .test_genius import genius, test_vcr
except ModuleNotFoundError:
    from test_genius import genius, test_vcr


class TestAPIBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n---------------------\nSetting up API base tests...\n")

    @test_vcr.use_cassette
    def test_http_error_handler(self):
        status_code = None
        try:
            genius.annotation(0)
        except HTTPError as e:
            status_code = e.args[0]

        self.assertEqual(status_code, 404)
