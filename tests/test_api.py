import unittest


from . import genius


class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n---------------------\nSetting up API tests...\n")

    def test_account(self):
        msg = ("No user detail was returned. "
               "Are you sure you're using a user access token?")
        r = genius.account()
        self.assertTrue("user" in r, msg)

    def test_annotation(self):
        msg = "Returned annotation API path is different than expected."
        id_ = 10225840
        r = genius.annotation(id_)
        real = r['annotation']['api_path']
        expected = '/annotations/10225840'
        self.assertEqual(real, expected, msg)

    def test_manage_annotation(self):
        example_text = 'The annotation'
        new_annotation = genius.create_annotation(
            example_text,
            'https://example.com',
            'illustrative examples',
            title='test')['annotation']
        msg = 'Annotation text did not match the one that was passed.'
        self.assertEqual(new_annotation['body']['plain'], example_text, msg)

        try:
            example_text_two = 'Updated annotation'
            r = genius.update_annotation(
                new_annotation['id'],
                example_text_two,
                'https://example.com',
                'illustrative examples',
                title='test'
            )['annotation']
            msg = 'Updated annotation text did not match the one that was passed.'
            self.assertEqual(r['body']['plain'], example_text_two, msg)

            r = genius.upvote_annotation(11828417)
            msg = 'Upvote was not registered.'
            self.assertTrue(r is not None, msg)

            r = genius.downvote_annotation(11828417)
            msg = 'Downvote was not registered.'
            self.assertTrue(r is not None, msg)

            r = genius.unvote_annotation(11828417)
            msg = 'Vote was not removed.'
            self.assertTrue(r is not None, msg)
        finally:
            msg = 'Annotation was not deleted.'
            r = genius.delete_annotation(new_annotation['id'])
            self.assertEqual(r, 204, msg)

    def test_referents_web_page(self):
        msg = "Returned referent API path is different than expected."
        id_ = 10347
        r = genius.referents(web_page_id=id_)
        real = r['referents'][0]['api_path']
        expected = '/referents/11828416'
        self.assertTrue(real == expected, msg)

    def test_referents_no_inputs(self):
        # Must supply `song_id`, `web_page_id`, or `created_by_id`.
        with self.assertRaises(AssertionError):
            genius.referents()

    def test_referents_invalid_input(self):
        # Method should prevent inputs for both song and web_pag ID.
        with self.assertRaises(AssertionError):
            genius.referents(song_id=1, web_page_id=1)

    def test_web_page(self):
        msg = "Returned web page API path is different than expected."
        url = "https://docs.genius.com"
        r = genius.web_page(raw_annotatable_url=url)
        real = r['web_page']['api_path']
        expected = '/web_pages/10347'
        self.assertEqual(real, expected, msg)
