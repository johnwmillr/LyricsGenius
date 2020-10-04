import unittest

from .test_api import TestAPI
from .test_artist import TestArtist
from .test_auth import TestOAuth2
from .test_base import TestAPIBase
from .test_genius import TestEndpoints, TestLyrics
from .test_public_methods import (
    TestAlbumMethods,
    TestAnnotationMethods,
    TestArticleMethods,
    TestArtistMethods,
    TestCoverArtMethods,
    TestDiscussionMethods,
    TestLeaderboardMethods,
    TestQuestionMethods,
    TestReferentMethods,
    TestSearchMethods,
    TestSongMethods,
    TestUserMethods,
    TestVideoMethods,
    TestMiscMethods,
)
from .test_song import TestSong
from .test_utils import TestUtils


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAPI())
    suite.addTest(TestArtist())
    suite.addTest(TestOAuth2())
    suite.addTest(TestAPIBase())
    suite.addTest(TestEndpoints())
    suite.addTest(TestLyrics())
    suite.addTest(TestSong())
    suite.addTest(TestUtils())
    suite.addTest(TestAlbumMethods())
    suite.addTest(TestAnnotationMethods())
    suite.addTest(TestArticleMethods())
    suite.addTest(TestArtistMethods())
    suite.addTest(TestCoverArtMethods())
    suite.addTest(TestDiscussionMethods())
    suite.addTest(TestLeaderboardMethods())
    suite.addTest(TestQuestionMethods())
    suite.addTest(TestReferentMethods())
    suite.addTest(TestSearchMethods())
    suite.addTest(TestSongMethods())
    suite.addTest(TestUserMethods())
    suite.addTest(TestVideoMethods())
    suite.addTest(TestMiscMethods())
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
