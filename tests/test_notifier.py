import unittest
from unittest.mock import patch
from notifier import prepare_message_and_url, MAX_MESSAGE_LENGTH, MAX_URL_LENGTH

class TestPrepareMessageAndUrl(unittest.TestCase):
    
    def test_normal_message_and_url(self):
        """Test case 1: Both message and URL are within limits"""
        message = "Breaking news: Important event happened"
        url = "https://example.com/article"
        
        result_msg, result_url = prepare_message_and_url(message, url)
        
        self.assertEqual(result_msg, message)
        self.assertEqual(result_url, url)
    
    def test_long_message_short_url(self):
        """Test case 2: Message exceeds MAX_MESSAGE_LENGTH, URL is short"""
        message = "x" * 1500  # 1500 chars, exceeds 1024 limit
        url = "https://example.com/short"
        
        result_msg, result_url = prepare_message_and_url(message, url)
        
        # Message should be truncated to 1021 chars + "..."
        self.assertEqual(len(result_msg), MAX_MESSAGE_LENGTH)
        self.assertTrue(result_msg.endswith("..."))
        self.assertEqual(result_url, url)
    
    def test_short_message_long_url_no_redirect(self):
        """Test case 3: URL exceeds MAX_URL_LENGTH, but final URL after redirect is short"""
        message = "Short message"
        long_url = "https://example.com/" + "x" * 600  # 619 chars, exceeds 512 limit
        final_url = "https://example.com/final"

        with patch('notifier.follow_redirects', return_value=final_url) as mock_follow:
            result_msg, result_url = prepare_message_and_url(message, long_url)

            self.assertEqual(result_msg, message)
            self.assertEqual(result_url, final_url)
            mock_follow.assert_called_once_with(long_url)
    
    def test_long_url_final_url_still_long_but_within_message_limit(self):
        """Test case 4: Final URL > 512 but <= 1024, should return URL as message"""
        message = "Important news"
        long_url = "https://example.com/" + "x" * 600
        final_url = "https://final.com/" + "y" * 700  # ~719 chars, > 512 but < 1024

        with patch('notifier.follow_redirects', return_value=final_url):
            result_msg, result_url = prepare_message_and_url(message, long_url)

            # Should return final URL as message, None for URL field
            self.assertEqual(result_msg, final_url)
            self.assertIsNone(result_url)
    
    def test_long_url_final_url_exceeds_message_limit(self):
        """Test case 5: Final URL > 1024, can't be returned anywhere"""
        message = "News article"
        long_url = "https://example.com/" + "x" * 600
        final_url = "https://final.com/" + "y" * 1500  # ~1519 chars, exceeds 1024

        with patch('notifier.follow_redirects', return_value=final_url):
            result_msg, result_url = prepare_message_and_url(message, long_url)

            # Should return message only, URL is lost
            self.assertEqual(result_msg, message)
            self.assertIsNone(result_url)
    
    def test_exact_max_message_length(self):
        """Test case 7: Message is exactly MAX_MESSAGE_LENGTH"""
        message = "x" * MAX_MESSAGE_LENGTH
        url = "https://example.com/short"
        
        result_msg, result_url = prepare_message_and_url(message, url)
        
        self.assertEqual(result_msg, message)
        self.assertEqual(result_url, url)
    
    def test_exact_max_url_length(self):
        """Test case 8: URL is exactly MAX_URL_LENGTH"""
        message = "Short message"
        # Build a URL that is exactly 512 chars
        base = "https://example.com/"
        padding_needed = MAX_URL_LENGTH - len(base)
        url = base + "x" * padding_needed
        
        self.assertEqual(len(url), MAX_URL_LENGTH)  # Verify it's exactly 512
        
        result_msg, result_url = prepare_message_and_url(message, url)
        
        self.assertEqual(result_msg, message)
        self.assertEqual(result_url, url)
    
    def test_url_one_char_over_limit(self):
        """Test case 9: URL is exactly one character over MAX_URL_LENGTH"""
        message = "Message"
        url = "https://example.com/" + "x" * (MAX_URL_LENGTH - 18)  # 513 chars
        final_url = "https://short.com"

        with patch('notifier.follow_redirects', return_value=final_url):
            result_msg, result_url = prepare_message_and_url(message, url)

            self.assertEqual(result_msg, message)
            self.assertEqual(result_url, final_url)

    def test_empty_message_and_url(self):
        """Test case 10: Edge case with empty strings"""
        message = ""
        url = ""
        
        result_msg, result_url = prepare_message_and_url(message, url)
        
        self.assertEqual(result_msg, "")
        self.assertEqual(result_url, "")


if __name__ == '__main__':
    unittest.main()
