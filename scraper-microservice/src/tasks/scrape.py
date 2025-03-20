from celery import Celery
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from scraper.scraper_categories import get_categories, scrape_top_apps, get_top_lists
from scraper.scraper_app_details import get_app_details
from config import MAX_THREADS, TIME_BETWEEN_REQUESTS
from tasks.save_to_mongo import save_categories_to_mongo, save_apps_to_mongo, save_app_details_to_mongo

# Celery configuration
celery_app = Celery(
    "tasks",
    broker="pyamqp://guest@rabbitmq//",
    backend="mongodb://mongo:27017/scraper_results"
)

# Logging configuration
logging.basicConfig(
    filename="logs/scraper_tasks.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


@celery_app.task
def scrape_categories():
    """Extracts categories from the App Store."""
    logging.info("🚀 Starting category extraction...")
    categories = get_categories()
    
    if not categories:
        logging.error("❌ No categories found!")
        return []
    
    logging.info(f"✅ {len(categories)} categories found.")

    # Save to MongoDB
    save_categories_to_mongo(categories)

    return categories


@celery_app.task
def scrape_apps_from_categories(categories):
    """Extracts top apps for each category."""
    all_apps = []
    logging.info("🚀 Starting app extraction...")

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {}
        for category_name, category_url in categories:
            free_apps_url, paid_apps_url = get_top_lists(category_name, category_url)
            if free_apps_url:
                futures[executor.submit(scrape_top_apps, category_name, "Top Free", free_apps_url)] = category_name
            if paid_apps_url:
                futures[executor.submit(scrape_top_apps, category_name, "Top Paid", paid_apps_url)] = category_name

        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    all_apps.extend(result)
                    logging.info(f"✅ {len(result)} apps extracted from category {futures[future]}.")
            except Exception as e:
                logging.error(f"❌ Error processing category {futures[future]}: {e}")

    logging.info(f"✅ Total of {len(all_apps)} apps collected.")

    # Save to MongoDB
    save_apps_to_mongo(all_apps)

    return all_apps


@celery_app.task
def scrape_app_details_parallel(apps):
    """Extracts app details in parallel."""
    all_details = []
    logging.info("🚀 Starting app details extraction...")

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {executor.submit(get_app_details, app["url"]): app for app in apps}
        for future in as_completed(futures):
            try:
                details = future.result()
                if details:
                    all_details.append(details)
            except Exception as e:
                logging.error(f"❌ Error fetching app details: {e}")
            time.sleep(TIME_BETWEEN_REQUESTS)

    logging.info(f"✅ Total of {len(all_details)} app details collected.")

    # Save to MongoDB
    save_app_details_to_mongo(all_details)

    return all_details
