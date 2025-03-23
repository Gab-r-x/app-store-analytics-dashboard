from datetime import datetime

def normalize_app_data(raw_app):
    """Normalize raw app data scraped from MongoDB."""
    url = raw_app.get("url") or raw_app.get("Url")

    return {
        "apple_id": extract_apple_id(url),
        "name": raw_app.get("Title"),
        "subtitle": raw_app.get("Subtitle"),
        "developer": raw_app.get("Developer"),
        "url": url,
        "icon_url": raw_app.get("icon_url"),

        # Ranking & Categorization
        "rank": safe_int(raw_app.get("rank")),
        "category_rank": raw_app.get("Category Rank"),
        "category": raw_app.get("category"),
        "list_type": raw_app.get("list_type"),

        # Monetization
        "price": raw_app.get("Price"),
        "has_in_app_purchases": detect_iap(raw_app),
        "monthly_revenue_estimate": safe_float(raw_app.get("monthly_revenue")),
        "monthly_downloads_estimate": safe_float(raw_app.get("monthly_downloads")),

        # Content
        "description": raw_app.get("Description"),
        "screenshots": raw_app.get("Screenshots"),
        "num_screenshots": len(raw_app.get("Screenshots") or []),
        "rating_summary": raw_app.get("Rating"),
        "latest_version": raw_app.get("Latest Version"),
        "latest_version_date": parse_date(raw_app.get("Latest Version Date")),

        # Additional
        "labels": raw_app.get("labels"),
        "reviews": raw_app.get("Reviews"),
        "privacy_data": raw_app.get("Privacy Data"),
        "general_info": raw_app.get("General Info"),
    }


def extract_apple_id(url):
    if not url:
        return None
    parts = url.split("id")
    return parts[-1] if len(parts) > 1 else None


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%b %d, %Y").date()
    except Exception:
        return None


def detect_iap(app):
    if not app:
        return None
    info = app.get("General Info") or app.get("general_info")
    return "Yes" if info and "In-App Purchases" in info else "No"


def safe_int(value):
    try:
        return int(value)
    except:
        return None


def safe_float(value):
    try:
        return float(value)
    except:
        return None
