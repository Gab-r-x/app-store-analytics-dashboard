import requests
import time
import random
from bs4 import BeautifulSoup
import logging
from config import USER_AGENTS, MAX_RETRIES, TIME_BETWEEN_REQUESTS

# Logging configuration
logging.basicConfig(
    filename="logs/scraper_app_details.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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

    # Title
    title = soup.find("h1", class_="product-header__title")
    details["Title"] = title.text.strip() if title else None
    
    # Subtitle
    subtitle = soup.find("h2", class_="product-header__subtitle")
    details["Subtitle"] = subtitle.text.strip() if subtitle else None
    
    # Developer
    developer = soup.find("h2", class_="product-header__identity")
    details["Developer"] = developer.text.strip() if developer else None
    
    # Category Rank
    category_rank = soup.select_one(".product-header__list__item a")
    details["Category Rank"] = category_rank.text.strip() if category_rank else None
    
    # Rating and Review Count
    rating_info = soup.select_one(".we-rating-count.star-rating__count")
    details["Rating"] = rating_info.text.strip() if rating_info else None
    
    # Price
    price_info = soup.select_one(".inline-list__item--bulleted")
    details["Price"] = price_info.text.strip() if price_info else None
    
    # Screenshots
    screenshots = []
    for picture in soup.select("picture.we-artwork"):
        sources = picture.find_all("source")
        best_quality = None
        for source in sources:
            srcset = source.get("srcset")
            if srcset:
                best_quality = srcset.split(",")[-1].strip().split(" ")[0]
        if best_quality:
            screenshots.append(best_quality)
    details["Screenshots"] = screenshots    
    
    # Description
    description = soup.select_one(".section__description p")
    details["Description"] = description.text.strip() if description else None
    
    # Latest Version and Release Date
    latest_version = soup.select_one(".whats-new__latest__version")
    latest_version_date = soup.select_one(".whats-new__latest time")
      
    details["Latest Version"] = latest_version.text.strip() if latest_version else None
    details["Latest Version Date"] = latest_version_date.text.strip() if latest_version_date else None
    
    # Reviews
    reviews = []
    reviews_page_url = app_url + "?see-all=reviews"
    response_reviews = requests.get(reviews_page_url, headers=get_headers())
    if response_reviews.status_code == 200:
        soup_reviews = BeautifulSoup(response_reviews.text, 'html.parser')
        for review in soup_reviews.select(".we-customer-review"):
            rating = review.select_one(".we-star-rating").get("aria-label") if review.select_one(".we-star-rating") else None
            author = review.select_one(".we-customer-review__user").text.strip() if review.select_one(".we-customer-review__user") else None
            date = review.select_one(".we-customer-review__date").text.strip() if review.select_one(".we-customer-review__date") else None
            title = review.select_one(".we-customer-review__title").text.strip() if review.select_one(".we-customer-review__title") else None
            body = review.select_one(".we-customer-review__body p").text.strip() if review.select_one(".we-customer-review__body p") else None
            reviews.append({"rating": rating, "author": author, "date": date, "title": title, "body": body})
    details["Reviews"] = reviews
    
    # Privacy Information
    privacy = []
    for item in soup.select(".privacy-type__data-category-heading"):
        privacy.append(item.text.strip())
    details["Privacy Data"] = privacy
    
    # General Information
    general_info = {}
    for info in soup.select(".information-list__item"):
        key = info.find("dt")
        value = info.find("dd")
        if key and value:
            general_info[key.text.strip()] = value.text.strip()
    details["General Info"] = general_info
    
    logging.info(f"✅ Data collected for app: {details.get('Title', 'Unknown')}")    
    
    random_delay()  # Adds delay to prevent blocking

    return details
