import requests
import time
import random
import unicodedata
from bs4 import BeautifulSoup
import logging
from config import settings
from bson import ObjectId  # Import para tratar ObjectId

USER_AGENTS = settings.USER_AGENTS
MAX_RETRIES = settings.MAX_RETRIES
TIME_BETWEEN_REQUESTS = settings.TIME_BETWEEN_REQUESTS

# Logging configuration
logging.basicConfig(
    filename="logs/scraper_app_details.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def clean_text(text):
    """Remove caracteres especiais e normaliza encoding."""
    if text:
        return unicodedata.normalize("NFKC", text).replace("\xa0", " ").strip()
    return None

def get_headers():
    """Returns a random User-Agent header to avoid blocking."""
    return {"User-Agent": random.choice(USER_AGENTS)}

def random_delay():
    """Applies a random delay between requests to prevent IP bans."""
    delay = random.uniform(*TIME_BETWEEN_REQUESTS)
    logging.info(f"Waiting {delay:.2f} seconds before the next request.")
    time.sleep(delay)

def get_page_with_retry(url):
    """Attempts to retrieve a webpage with automatic retries for 429 errors."""
    attempt = 0
    while attempt < MAX_RETRIES:
        response = requests.get(url, headers=get_headers())
        response.encoding = 'utf-8'

        if response.status_code == 200:
            return response
        
        elif response.status_code == 429:
            wait_time = 2 ** attempt  # Exponential backoff (2s, 4s, 8s...)
            logging.warning(f"⚠️ Rate limited (429) at {url}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

        else:
            logging.error(f"❌ Error accessing {url}: {response.status_code}")
            return None
        
        attempt += 1
    
    logging.error(f"🚨 Failed after {MAX_RETRIES} attempts. Skipping {url}.")
    return None

def get_app_details(app_url):
    """Scrapes app details from the App Store."""
    logging.info(f'🔍 Scraping: {app_url}')
    response = get_page_with_retry(app_url)
    if not response:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    details = {}

    # title
    title = soup.find("h1", class_="product-header__title")
    details["Title"] = clean_text(title.text) if title else None
    
    # subtitle
    subtitle = soup.find("h2", class_="product-header__subtitle")
    details["Subtitle"] = clean_text(subtitle.text) if subtitle else None
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # icon
    icon_el = soup.select_one("picture.we-artwork source[type='image/png']")
    if icon_el:
        icon_url = icon_el.get("srcset", "").split(",")[-1].strip().split(" ")[0]
        details["icon_url"] = icon_url
    else:
        details["icon_url"] = None

    # developer
    developer = soup.find("h2", class_="product-header__identity")
    details["Developer"] = clean_text(developer.text) if developer else None
    
    # app url
    details["Url"] = app_url

    # category_rank
    category_rank = soup.select_one(".product-header__list__item a")
    details["Category Rank"] = clean_text(category_rank.text) if category_rank else None

    # rating
    rating_info = soup.select_one(".we-rating-count.star-rating__count")
    details["Rating"] = clean_text(rating_info.text) if rating_info else None

    # price
    price_info = soup.select_one(".inline-list__item--bulleted")
    details["Price"] = clean_text(price_info.text) if price_info else None

    # screenshots
    screenshots = []
    for picture in soup.select('picture.we-artwork--screenshot-platform-iphone'):
        sources = picture.find_all("source")
        best_quality = None
        for source in sources:
            srcset = source.get("srcset")
            if srcset:
                best_quality = srcset.split(",")[-1].strip().split(" ")[0]
        if best_quality:
            screenshots.append(best_quality)
    details["Screenshots"] = screenshots    

    # description
    description_container = soup.select_one(".we-truncate--multi-line")

    if description_container:
        paragraphs = description_container.find_all("p")
        description = "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
        details["Description"] = description
    else:
        details["Description"] = None

    # last version
    latest_version = soup.select_one(".whats-new__latest__version")
    latest_version_date = soup.select_one(".whats-new__latest time")
      
    details["Latest Version"] = clean_text(latest_version.text) if latest_version else None
    details["Latest Version Date"] = clean_text(latest_version_date.text) if latest_version_date else None

    # reviews
    reviews = []
    reviews_page_url = app_url + "?see-all=reviews"
    response_reviews = requests.get(reviews_page_url, headers=get_headers())
    response.encoding = 'utf-8'

    if response_reviews.status_code == 200:
        soup_reviews = BeautifulSoup(response_reviews.text, 'html.parser')
        for review in soup_reviews.select(".we-customer-review"):
            reviews.append({
                "rating": clean_text(review.select_one(".we-star-rating").get("aria-label")) if review.select_one(".we-star-rating") else None,
                "author": clean_text(review.select_one(".we-customer-review__user").text) if review.select_one(".we-customer-review__user") else None,
                "date": clean_text(review.select_one(".we-customer-review__date").text) if review.select_one(".we-customer-review__date") else None,
                "title": clean_text(review.select_one(".we-customer-review__title").text) if review.select_one(".we-customer-review__title") else None,
                "body": clean_text(review.select_one(".we-customer-review__body p").text) if review.select_one(".we-customer-review__body p") else None
            })
    details["Reviews"] = reviews

    # privacy
    privacy = []
    for item in soup.select(".privacy-type__data-category-heading"):
        privacy.append(clean_text(item.text))
    details["Privacy Data"] = privacy

    # general info
    general_info = {}
    for info in soup.select(".information-list__item"):
        key = info.find("dt")
        value = info.find("dd")
        if key and value:
            general_info[clean_text(key.text)] = clean_text(value.text)
    details["General Info"] = general_info

    logging.info(f"✅ Data collected for app: {details.get('Title', 'Unknown')}")    

    random_delay()  # Adds delay to prevent blocking

    return details
