import requests
from typing import List

def send_notification(title: str, message: str, url: str, user_keys: List[str], api_token: str):
    api_url = "https://api.pushover.net/1/messages.json"
    
    for user_key in user_keys:
        data = {
            "token": api_token,
            "user": user_key,
            "title": title,
            "message": message,
            "url": url,
            "url_title": "Read more"
        }
        
        try:
            response = requests.post(api_url, data=data)
            response.raise_for_status()
            print(f"Notification sent to {user_key}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send notification to {user_key}: {e}")
