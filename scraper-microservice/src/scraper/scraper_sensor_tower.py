import time
import logging
from bs4 import BeautifulSoup
from scraper.sensor_tower_client import login_to_sensortower
from config import settings
import random

# Logging
logger = logging.getLogger(__name__)
TIME_BETWEEN_REQUESTS = settings.TIME_BETWEEN_REQUESTS

def clean_text(text):
    """Sanitize and normalize string values."""
    if text:
        return text.replace('\xa0', ' ').strip()
    return None

def random_delay():
    """Sleep between 1-2 seconds to avoid rate limiting."""
    delay = random.uniform(*TIME_BETWEEN_REQUESTS)
    logger.info(f"⏳ Waiting {delay:.2f}s between requests to avoid blocking...")
    time.sleep(delay)

def get_sensor_tower_data(session, apple_id: str) -> dict:
    """Scrapes download and revenue data for a single app from Sensor Tower."""
    url = f"https://app.sensortower.com/overview/{apple_id}?country=US"
    logger.info(f"🔍 Scraping Sensor Tower for Apple ID: {apple_id}")

    try:
        response = session.get(url)
        if response.status_code != 200:
            logger.warning(f"⚠️ Failed to fetch data for {apple_id} - Status: {response.status_code}")
            return {}

        soup = BeautifulSoup(response.text, "html.parser")

        downloads_el = soup.select_one("h4#app-overview-unified-kpi-downloads + p + span")
        revenue_el = soup.select_one("h4#app-overview-unified-kpi-revenue + p + span")

        downloads = clean_text(downloads_el.text) if downloads_el else None
        revenue = clean_text(revenue_el.text) if revenue_el else None

        logger.info(f"✅ Apple ID {apple_id} - Downloads: {downloads}, Revenue: {revenue}")
        return {
            "apple_id": apple_id,
            "monthly_downloads_estimate": downloads,
            "monthly_revenue_estimate": revenue
        }

    except Exception as e:
        logger.error(f"❌ Error scraping {apple_id}: {e}")
        return {}

def scrape_sensor_tower_for_all(app_ids: list) -> list:
    """Performs sequential scraping for a list of Apple IDs."""
    session = login_to_sensortower()
    if not session:
        logger.error("🚫 Cannot proceed without authenticated session.")
        return []

    results = []
    for app_id in app_ids:
        data = get_sensor_tower_data(session, app_id)
        if data:
            results.append(data)
        random_delay()

    return results
