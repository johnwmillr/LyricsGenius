import unittest

from lyricsgenius.utils import (
    auth_from_environment,
    decode_js_string,
    parse_redirected_url,
    sanitize_filename,
)


class TestUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n---------------------\nSetting up utils tests...\n")

    def test_sanitize_filename(self):
        raw = "B<ad File|_name"
        cleaned = "Bad File_name"
        r = sanitize_filename(raw)
        self.assertEqual(r, cleaned)

    def test_decode_js_string(self):
        cases = [
            (r"plain", "plain"),
            (r"it\'s \"quoted\" \/ \\", 'it\'s "quoted" / \\'),
            (r"\x41\u0042\u{43}", "ABC"),
            (r"line\nbreak\ttab", "line\nbreak\ttab"),
            (r"\uD83C\uDFB5", "\U0001f3b5"),
            ("continued\\\nline", "continuedline"),
            (r"\q", "q"),
        ]
        for literal, expected in cases:
            with self.subTest(literal=literal):
                self.assertEqual(decode_js_string(literal), expected)

    def test_parse_redirected_url(self):
        redirected = "https://example.com/callback?code=test"
        flow = "code"
        code = "test"
        r = parse_redirected_url(redirected, flow)
        self.assertEqual(r, code)

        redirected = "https://example.com/callback#access_token=test"
        flow = "token"
        code = "test"
        r = parse_redirected_url(redirected, flow)
        self.assertEqual(r, code)

    def test_auth_from_environment(self):
        credentials = auth_from_environment()
        self.assertTrue(len(credentials) == 3)
