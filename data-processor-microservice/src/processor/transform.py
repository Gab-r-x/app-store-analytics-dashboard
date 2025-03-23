import re
import unicodedata
import json

def transform_app_data(app_data):
    """Apply transformations to normalized app data."""
    transformed = app_data.copy()

    # Normalize common text fields
    text_fields = ["name", "subtitle", "developer", "description", "rating_summary"]
    for field in text_fields:
        if transformed.get(field):
            transformed[field] = clean_text(transformed[field])

    # Normalize reviews (try parse if string)
    reviews = transformed.get("reviews")
    if isinstance(reviews, str):
        try:
            reviews = json.loads(reviews)
        except Exception:
            reviews = []
    if isinstance(reviews, list):
        transformed["reviews"] = [clean_review(r) for r in reviews]

    # Normalize general_info (try parse if string)
    general_info = transformed.get("general_info")
    if isinstance(general_info, str):
        try:
            general_info = json.loads(general_info)
        except Exception:
            general_info = {}
    if isinstance(general_info, dict):
        transformed["general_info"] = {
            clean_text(k): clean_text(v) for k, v in general_info.items()
        }

    return transformed


def clean_text(text):
    """Normalize and clean string data to UTF-8 safe and readable format."""
    if not isinstance(text, str):
        return text
    text = unicodedata.normalize("NFKC", text)
    text = text.encode("utf-8", errors="ignore").decode("utf-8")
    return re.sub(r"\s+", " ", text).strip()


def clean_review(review):
    return {
        "rating": clean_text(review.get("rating")),
        "author": clean_text(review.get("author")),
        "date": clean_text(review.get("date")),
        "title": clean_text(review.get("title")),
        "body": clean_text(review.get("body")),
    }
