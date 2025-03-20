from celery import Celery
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from scraper.scraper_categories import get_categories, scrape_top_apps, get_top_lists
from scraper.scraper_app_details import get_app_details
from config import settings
from tasks.save_to_mongo import save_categories_to_mongo, save_apps_to_mongo, save_app_details_to_mongo

# Celery configuration
celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["tasks.scrape", "tasks.save_to_mongo"],
    task_serializer="pickle",
    result_serializer="pickle",
    accept_content=["pickle", "json"],
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

    max_threads = settings.get("MAX_THREADS", 8)  # Default: 8 threads

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
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

    max_threads = settings.get("MAX_THREADS", 8)
    time_between_requests = settings.get("TIME_BETWEEN_REQUESTS", [1, 3])

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(get_app_details, app["url"]): app for app in apps}
        for future in as_completed(futures):
            try:
                details = future.result()
                if details:
                    all_details.append(details)
            except Exception as e:
                logging.error(f"❌ Error fetching app details: {e}")
            
            time.sleep(time_between_requests[0])  # Minimum delay

    logging.info(f"✅ Total of {len(all_details)} app details collected.")

    # Save to MongoDB
    save_app_details_to_mongo(all_details)

    return all_details
