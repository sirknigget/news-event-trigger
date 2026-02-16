import logging
from src.config import load_config
from src.rss import fetch_rss_events
from src.classifier import classify_event
from src.notifier import send_notification

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        config = load_config()
        logging.info("Configuration loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to load configuration: {e}")
        return

    logging.info(f"Fetching RSS feed from {config.rss_feed_url}")
    try:
        events = fetch_rss_events(config.rss_feed_url, config.lookback_minutes, config.keyword_filter)
    except Exception as e:
        logging.error(f"Failed to fetch RSS feed: {e}")
        return


    logging.info(f"Found {len(events)} events matching keyword '{config.keyword_filter}' in the last {config.lookback_minutes} minutes.")
    logging.info(f"Expected triggering event: {config.triggering_event}")
    for event in events:
        try:
            logging.info(f"Classifying event: {event.title}")
            is_triggered = classify_event(event.title, event.description, config)

            if is_triggered:
                logging.info("TRIGGERED")
                send_notification(
                    title=f"News Alert: {config.keyword_filter}",
                    message=event.title,
                    url=event.link,
                    user_keys=config.pushover_user_keys,
                    api_token=config.pushover_api_token
                )
            else:
                logging.info("Not triggered")
        except Exception as e:
            logging.error(f"Error processing event '{event.title}': {e}")

if __name__ == "__main__":
    main()
