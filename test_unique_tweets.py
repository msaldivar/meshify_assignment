#!/usr/bin/python3

import unittest
import multiprocessing
import unique_tweets


class UniqueTweetsTests(unittest.TestCase):
    """Tests for unique_tweets.py"""

    def test_twitter_package(self):
        """check if package is present"""
        is_present = False
        try:
            import twitter
        except ImportError:
            is_present = False
        else:
            is_present = True
        self.assertTrue(is_present, 'run: pip install twitter')

    def test_twitter_credentials(self):
        """test api credentials"""
        self.assertTrue(unique_tweets.credentials_check())

    def test_twitter_search(self):
        """default return length is 15 """
        results = unique_tweets.api.GetSearch("#IOT")
        self.assertEqual(len(results), 15)

    def test_get_thread_count(self):
        """test the returned value of get_thread_count()"""
        thread_num = unique_tweets.get_thread_count()
        self.assertEqual(thread_num, multiprocessing.cpu_count())


if __name__ == '__main__':
    unittest.main()
