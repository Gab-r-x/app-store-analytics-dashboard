import time
import logging
import random
from bs4 import BeautifulSoup
from config import settings
from scraper.sensor_tower_client import login_with_selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tasks.save_to_mongo import save_sensor_metrics_to_mongo

# Logging
logger = logging.getLogger(__name__)
TIME_BETWEEN_REQUESTS = settings.TIME_BETWEEN_REQUESTS

def clean_text(text):
    if text:
        return text.replace('\xa0', ' ').strip()
    return None

def random_delay():
    delay = 10 + random.uniform(*TIME_BETWEEN_REQUESTS)
    logger.info(f"⏳ Waiting {delay:.2f}s between requests to avoid blocking...")
    time.sleep(delay)

def get_sensor_tower_data(driver, apple_id: str) -> dict:
    """Scrapes download and revenue data using an authenticated Selenium session."""
    url = f"https://app.sensortower.com/overview/{apple_id}?country=US"
    logger.info(f"🌐 Scraping Sensor Tower for Apple ID: {apple_id}")

    for attempt in range(2):  # Retry up to 2 times
        try:
            driver.get(url)

            wait = WebDriverWait(driver, 15)

            # Wait for both elements
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span[aria-labelledby="app-overview-unified-kpi-downloads"]')))
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span[aria-labelledby="app-overview-unified-kpi-revenue"]')))

            soup = BeautifulSoup(driver.page_source, "html.parser")

            downloads_el = soup.select_one('span[aria-labelledby="app-overview-unified-kpi-downloads"]')
            revenue_el = soup.select_one('span[aria-labelledby="app-overview-unified-kpi-revenue"]')

            downloads = clean_text(downloads_el.text) if downloads_el else None
            revenue = clean_text(revenue_el.text) if revenue_el else None

            if downloads or revenue:
                logger.info(f"✅ Apple ID {apple_id} - Downloads: {downloads}, Revenue: {revenue}")
                return {
                    "apple_id": apple_id,
                    "monthly_downloads_estimate": downloads,
                    "monthly_revenue_estimate": revenue
                }
            else:
                logger.warning(f"⚠️ Apple ID {apple_id} - Elements found but values were empty.")
                return {}

        except Exception as e:
            logger.warning(f"🔁 Attempt {attempt + 1} failed for {apple_id}: {e}")
            if attempt == 0:
                logger.info("⏱ Waiting 60 seconds before retrying...")
                time.sleep(60)
            else:
                logger.error(f"❌ Failed after retrying for Apple ID: {apple_id}")
                return {}

def scrape_sensor_tower_for_all(app_ids: list, current_app) -> list:
    """Sequentially scrapes a list of Apple IDs using a single logged-in Selenium session."""
    driver = login_with_selenium()
    if not driver:
        logger.error("🚫 Could not start Selenium session or login failed.")
        return []

    results = []
    for app_id in app_ids:
        data = get_sensor_tower_data(driver, app_id)
        if data:
            results.append(data)
            save_sensor_metrics_to_mongo(data)
            current_app.send_task("tasks.process_data.run_sensor_metrics_processing", queue="data_processor")

        random_delay()

    driver.quit()
    return results
