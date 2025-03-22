def normalize_app_data(raw_app):
    """Normalize raw app data scraped from MongoDB."""
    return {
        "apple_id": extract_apple_id(raw_app.get("url")),
        "name": raw_app.get("Title"),
        "subtitle": raw_app.get("Subtitle"),
        "developer": raw_app.get("Developer"),
        "url": raw_app.get("url"),
        "icon_url": raw_app.get("icon_url"),
        "rank": safe_int(raw_app.get("rank")),
        "category_rank": raw_app.get("Category Rank"),
        "category": raw_app.get("category"),
        "list_type": raw_app.get("list_type"),
        "price": raw_app.get("Price"),
        "has_in_app_purchases": detect_iap(raw_app),
        "monthly_revenue_estimate": raw_app.get("monthly_revenue"),
        "monthly_downloads_estimate": raw_app.get("monthly_downloads"),
        "description": raw_app.get("Description"),
        "screenshots": raw_app.get("Screenshots"),
        "num_screenshots": len(raw_app.get("Screenshots", [])),
        "rating_summary": raw_app.get("Rating"),
        "latest_version": raw_app.get("Latest Version"),
        "latest_version_date": parse_date(raw_app.get("Latest Version Date")),
        "labels": raw_app.get("labels"),
        "reviews": raw_app.get("Reviews"),
        "privacy_data": raw_app.get("Privacy Data"),
        "general_info": raw_app.get("General Info")
    }


def extract_apple_id(url):
    if not url:
        return None
    parts = url.split("id")
    return parts[-1] if len(parts) > 1 else None

def parse_date(date_str):
    from datetime import datetime
    try:
        return datetime.strptime(date_str, "%b %d, %Y").date()
    except Exception:
        return None

def detect_iap(app):
    if not app:
        return None
    iap_flag = app.get("general_info", {}).get("In-App Purchases")
    return "Yes" if iap_flag else "No"

def safe_int(value):
    try:
        return int(value)
    except:
        return None
