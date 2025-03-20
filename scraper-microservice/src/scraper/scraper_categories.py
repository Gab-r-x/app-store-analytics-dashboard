import time
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin
import logging
from config import settings

# Load settings from Dynaconf
BASE_URL = settings.BASE_URL
USER_AGENTS = settings.USER_AGENTS
TIME_BETWEEN_REQUESTS = settings.TIME_BETWEEN_REQUESTS
MAX_THREADS = settings.MAX_THREADS

# Logging configuration
logging.basicConfig(
    filename="logs/scraper_categories.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Selenium configuration
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Use fixed ChromeDriver path (avoid WebDriver Manager)
service = Service("/usr/bin/chromedriver")  
driver = webdriver.Chrome(service=service, options=chrome_options)

# Persistent session for requests
session = requests.Session()

def get_headers():
    """Returns a random User-Agent header to prevent blocking."""
    return {"User-Agent": random.choice(USER_AGENTS)}

def random_delay():
    """Applies a random delay between requests to mimic human behavior."""
    delay = random.uniform(*TIME_BETWEEN_REQUESTS)
    logging.info(f"Waiting {delay:.2f} seconds before the next request.")
    time.sleep(delay)

def get_categories():
    """Scrapes all categories and their URLs from the App Store."""
    logging.info("Opening App Store categories page...")
    driver.get(BASE_URL + "/us/charts/iphone/top-free-apps/36")
    time.sleep(2)

    try:
        category_button = driver.find_element(By.CSS_SELECTOR, "button.we-genre-filter__pill")
        ActionChains(driver).move_to_element(category_button).click().perform()
        time.sleep(1)

        logging.info("Extracting categories...")
        category_links = []
        category_elements = driver.find_elements(By.CSS_SELECTOR, "a.we-genre-filter__item")
        for category in category_elements:
            category_name = category.text.strip()
            category_url = urljoin(BASE_URL, category.get_attribute("href"))
            if category_name and category_url:
                category_links.append((category_name, category_url))

        logging.info(f"✅ Found {len(category_links)} categories.")
        return category_links

    except Exception as e:
        logging.error(f"❌ Error extracting categories: {e}")
        return []

def get_top_lists(category_name, category_url):
    """Gets the Top Free and Top Paid app list URLs for a given category."""
    logging.info(f"Extracting app lists for category: {category_name}...")

    response = session.get(category_url, headers=get_headers())
    if response.status_code != 200:
        logging.error(f"❌ Error accessing {category_url}: {response.status_code}")
        return None, None

    soup = BeautifulSoup(response.text, 'html.parser')
    free_apps_link, paid_apps_link = None, None
    links = soup.find_all("a", class_="section__headline-link")

    for link in links:
        h2 = link.find("h2", class_="section__headline")
        if h2:
            if "Top Free Apps" in h2.text:
                free_apps_link = urljoin(BASE_URL, link["href"])
            elif "Top Paid Apps" in h2.text:
                paid_apps_link = urljoin(BASE_URL, link["href"])

    return free_apps_link, paid_apps_link

def scrape_top_apps(category_name, list_type, list_url):
    """Scrapes the top 100 apps from a category's list (Free/Paid)."""
    logging.info(f"Scraping apps for category {category_name} - {list_type}")

    response = session.get(list_url, headers=get_headers())
    if response.status_code != 200:
        logging.error(f"❌ Error accessing {list_url}: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    apps = soup.find_all("li", class_="l-column--grid")
    app_data = []

    for app in apps[:100]:  # Limit to the top 100 apps
        rank = app.find("p", class_="we-lockup__rank")
        title = app.find("div", class_="we-lockup__title")
        developer = app.find("div", class_="we-lockup__subtitle")
        link = app.find("a", class_="we-lockup")

        app_data.append({
            "category": category_name,
            "list_type": list_type,
            "rank": rank.text.strip() if rank else "Unknown Rank",
            "name": title.text.strip() if title else "Unknown Title",
            "developer": developer.text.strip() if developer else "Unknown Developer",
            "url": urljoin(BASE_URL, link["href"]) if link else "No URL"
        })

    logging.info(f"✅ Scraped {len(app_data)} apps from {category_name} - {list_type}.")
    
    random_delay()  

    return app_data
