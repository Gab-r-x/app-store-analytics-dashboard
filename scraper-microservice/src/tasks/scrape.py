from celery import Celery, current_app
import logging
import time
import re
from config import settings
from tasks.progress_tracker import init_scrape_progress, mark_category_done
from database.get_mongo import get_mongo_collection
from concurrent.futures import ThreadPoolExecutor, as_completed
from scraper.scraper_categories import get_categories, scrape_top_apps, get_top_lists
from scraper.scraper_app_details import get_app_details
from scraper.scraper_sensor_tower import scrape_sensor_tower_for_all
from tasks.save_to_mongo import save_categories_to_mongo, save_apps_to_mongo, save_app_details_to_mongo, save_sensor_metrics_to_mongo

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

@celery_app.task(queue="app_details")
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
        
    category_names = [cat[0] for cat in categories]
    init_scrape_progress(category_names)

    # Dispatch a scrape_category_apps task for each category
    for category in categories:
        scrape_category_apps.delay(category)

    return categories


@celery_app.task(queue="app_details")
def scrape_category_apps(category):
    """Extracts apps for a single category and chains the details scraping."""
    category_name, category_url = category
    logging.info(f"📂 Scraping category: {category_name}")

    free_apps_url, paid_apps_url = get_top_lists(category_name, category_url)
    apps = []

    if free_apps_url:
        apps += scrape_top_apps(category_name, "Top Free", free_apps_url)
    if paid_apps_url:
        apps += scrape_top_apps(category_name, "Top Paid", paid_apps_url)

    if not apps:
        logging.warning(f"⚠️ No apps found for category {category_name}.")
        mark_category_done(category_name)
        return

    save_apps_to_mongo(apps)
    logging.info(f"✅ Saved {len(apps)} apps for category {category_name}.")

    # Extract URLs and dispatch task to get details
    apps_urls = [{"url": app["url"]} for app in apps if "url" in app]
    scrape_app_details_for_category.apply_async((apps_urls,), queue="app_details")

    # Mark as processed
    mark_category_done(category_name)

@celery_app.task(rate_limit="24/h", queue="app_details")
def scrape_app_details_for_category(apps):
    all_details = []
    logging.info("🔍 Scraping app details for a category batch...")

    max_threads = settings.get("MAX_THREADS", 2)
    time_between_requests = settings.get("TIME_BETWEEN_REQUESTS", [2, 5])

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(get_app_details, app["url"]): app for app in apps}
        for future in as_completed(futures):
            try:
                details = future.result()
                if details:
                    all_details.append(details)
            except Exception as e:
                logging.error(f"❌ Error fetching app details: {e}")

            time.sleep(time_between_requests[0])

    logging.info(f"✅ Collected {len(all_details)} app details in category batch.")
    save_app_details_to_mongo(all_details)
    current_app.send_task("tasks.process_data.run_data_processing", queue="data_processor")

@celery_app.task(queue="app_details")
def scrape_sensor_tower_data():
    """Scrapes Sensor Tower data (downloads & revenue) for all apps in raw_apps."""
    logging.info("📊 Starting Sensor Tower data scraping...")

    collection = get_mongo_collection("raw_apps")
    cursor = collection.find({}, {"url": 1})
    urls = [doc["url"] for doc in cursor if "url" in doc]

    if not urls:
        logging.warning("⚠️ No app URLs found to scrape Sensor Tower data.")
        return

    # Extrai apple_ids válidos das URLs
    apple_ids = []
    for url in urls:
        match = re.search(r'id(\d+)', url)
        if match:
            apple_ids.append(match.group(1))
        else:
            logging.warning(f"⚠️ Could not extract apple_id from URL: {url}")

    if not apple_ids:
        logging.warning("⚠️ No valid Apple IDs extracted.")
        return

    results = scrape_sensor_tower_for_all(apple_ids)

    if results:
        # save_sensor_metrics_to_mongo(results)
        logging.info(f"✅ Saved Sensor Tower data for {len(results)} apps.")
    else:
        logging.warning("⚠️ No Sensor Tower data scraped.")
