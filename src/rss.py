import feedparser
from datetime import datetime, timedelta, timezone
from dateutil import parser as date_parser
from typing import List, Optional
from dataclasses import dataclass

from bs4 import BeautifulSoup

@dataclass
class NewsEvent:
    title: str
    link: str
    description: str
    published: datetime

def strip_html(html_content: str) -> str:
    if not html_content:
        return ""
    return BeautifulSoup(html_content, "html.parser").get_text(separator=" ", strip=True)

def fetch_rss_events(feed_url: str, lookback_minutes: int, keyword_filter: Optional[str] = None) -> List[NewsEvent]:
    feed = feedparser.parse(feed_url)
    events = []
    
    now = datetime.now(timezone.utc)
    cutoff_time = now - timedelta(minutes=lookback_minutes)

    for entry in feed.entries:
        # Parse published date. Handle different formats if needed, but dateutil is robust.
        try:
            published_time = date_parser.parse(entry.published)
            # Ensure timezone awareness
            if published_time.tzinfo is None:
                published_time = published_time.replace(tzinfo=timezone.utc)
        except (AttributeError, ValueError):
            continue # Skip if no date found

        if published_time < cutoff_time:
            continue

        title = entry.get("title", "")

        if keyword_filter:
            if keyword_filter.lower() not in title.lower():
                continue

        events.append(NewsEvent(
            title=title,
            link=entry.get("link", ""),
            description="",
            published=published_time
        ))
    
    return events
