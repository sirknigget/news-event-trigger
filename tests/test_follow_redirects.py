import unittest

from follow_redirects import follow_redirects


class TestFollowRedirects(unittest.TestCase):

    def test_real_google_news_url(self):
        google_news_url = "https://news.google.com/rss/articles/CBMiswFBVV95cUxQeXhyS0xzNm5NSWozN2RYUmgxb0daZy1lUHl1Rm5PX3dxMEdmcTN5TGZZWUF2V2JMM1JxNE9hcld1NEdHbUVtYXlPQ2taVHVEeTRYakc4ZnRUZTNiWFdXenp1dXYtbU5yT2VtcGdzOTBGSjJYOFF2NzVrdDQ2RXo1WUVwdWNvNE40NHZGSnAyQ2JMdVNhcjlUdHEzdl9kLTlaTDhMdjVSWXJvYW5oY20yRHFzWdIBuAFBVV95cUxOeDBveEpWWlBIVlJjZy1Jdmk3WUQ3MDJfMXRmM1FMSWJma2kxRzJqTGwzZjYzaXdKaU5LNmtfM21JTTlhd3RPOG5PMldLNzBqVjZTT0tyYmRpV0NGTUtaLVNxbXRzZHJPUV9WUnhLYzRXci1wVmdBaHNJUmI4Nkt4THVJNFdlckJZQmJ2MUkzazBpUHJPN0JnMUtvNXpha2k3QzV3bHRMbjEtbXZhNDg5c0RDbVgwcUVH?oc=5"
        result_url = follow_redirects(google_news_url)

        # The final URL should not be a Google News URL
        self.assertIsNotNone(result_url)
        self.assertNotIn("news.google.com", result_url)