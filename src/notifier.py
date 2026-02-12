import requests
from typing import List, Optional, Tuple

# Pushover limits
MAX_MESSAGE_LENGTH = 1024
MAX_URL_LENGTH = 512

def prepare_message_and_url(message: str, url: str) -> Tuple[str, Optional[str]]:
    """
    Prepare message and URL for Pushover, handling length limits.
    
    Args:
        message: The notification message
        url: The URL to include
        
    Returns:
        Tuple of (prepared_message, prepared_url). 
        If URL is None, it means the URL was embedded in the message instead.
    """
    # Step 1: Truncate message to max length if needed
    if len(message) > MAX_MESSAGE_LENGTH:
        message = message[:MAX_MESSAGE_LENGTH - 3] + "..."
    
    # Step 2: If URL is already within limits, return as is
    if len(url) <= MAX_URL_LENGTH:
        return message, url
    
    # Step 3: Follow redirects to get final URL
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        final_url = response.url
    except requests.exceptions.RequestException:
        # If we can't follow redirects, use the original URL
        final_url = url
    
    # If final URL is within limits, return it
    if len(final_url) <= MAX_URL_LENGTH:
        return message, final_url
    
    # Step 4: Final URL is still too long, embed it in the message
    # Calculate available space: MAX_MESSAGE_LENGTH - "... " - final_url
    url_with_separator = "... " + final_url
    if (len(message) + len(url_with_separator)) > MAX_MESSAGE_LENGTH:
        return message, None
    return message + url_with_separator, None

def send_notification(title: str, message: str, url: str, user_keys: List[str], api_token: str):
    api_url = "https://api.pushover.net/1/messages.json"
    
    # Prepare message and URL to handle Pushover limits
    prepared_message, prepared_url = prepare_message_and_url(message, url)
    
    for user_key in user_keys:
        data = {
            "token": api_token,
            "user": user_key,
            "title": title,
            "message": prepared_message,
        }
        
        # Only include URL fields if we have a separate URL (not embedded in message)
        if prepared_url is not None:
            data["url"] = prepared_url
            data["url_title"] = "Read more"
        
        try:
            response = requests.post(api_url, data=data)
            response.raise_for_status()
            print(f"Notification sent to {user_key}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send notification to {user_key}: {e}")
