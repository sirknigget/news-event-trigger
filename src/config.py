import json
import os
from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    rss_feed_url: str
    keyword_filter: str
    triggering_event: str
    lookback_minutes: int
    pushover_user_keys: List[str]
    pushover_api_token: str
    openai_api_key: str

def load_config(config_path: str = "config.json") -> Config:
    with open(config_path, "r") as f:
        config_data = json.load(f)

    pushover_api_token = os.getenv("PUSHOVER_API_TOKEN")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    pushover_user_keys_str = os.getenv("PUSHOVER_USER_KEYS", "")
    pushover_user_keys = [k.strip() for k in pushover_user_keys_str.split(",") if k.strip()]

    if not pushover_api_token:
        raise ValueError("PUSHOVER_API_TOKEN environment variable is not set")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    if not pushover_user_keys:
         # Fallback to config for backward compatibility or raise error? 
         # Plan said to move it, so let's check config as fallback but prefer env.
         pushover_user_keys = config_data.get("pushover_user_keys", [])
         
    if not pushover_user_keys:
        raise ValueError("PUSHOVER_USER_KEYS environment variable is not set")

    keyword = config_data["keyword_filter"]
    rss_url = config_data["rss_feed_url"]
    if "{keyword}" in rss_url:
        rss_url = rss_url.format(keyword=keyword)

    return Config(
        rss_feed_url=rss_url,
        keyword_filter=keyword,
        triggering_event=config_data["triggering_event"],
        lookback_minutes=config_data.get("lookback_minutes", 60),
        pushover_user_keys=pushover_user_keys,
        pushover_api_token=pushover_api_token,
        openai_api_key=openai_api_key,
    )
