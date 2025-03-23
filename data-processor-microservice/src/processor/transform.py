import re
import unicodedata

def transform_app_data(app_data):
    """Apply transformations to normalized app data."""
    transformed = app_data.copy()

    # Normalize common text fields
    text_fields = ["name", "subtitle", "developer", "description", "rating_summary"]
    for field in text_fields:
        if transformed.get(field):
            transformed[field] = clean_text(transformed[field])

    # Normalize reviews
    if isinstance(transformed.get("reviews"), list):
        transformed["reviews"] = [clean_review(r) for r in transformed["reviews"]]

    # Normalize general_info
    if isinstance(transformed.get("general_info"), dict):
        transformed["general_info"] = {
            clean_text(k): clean_text(v) for k, v in transformed["general_info"].items()
        }

    return transformed


def clean_text(text):
    """Normalize and clean string data to UTF-8 safe and readable format."""
    if not isinstance(text, str):
        return text
    text = unicodedata.normalize("NFKC", text)
    text = text.encode("utf-8", errors="ignore").decode("utf-8")  # Safe re-encoding
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_review(review):
    """Sanitize review fields."""
    return {
        "rating": clean_text(review.get("rating")),
        "author": clean_text(review.get("author")),
        "date": clean_text(review.get("date")),
        "title": clean_text(review.get("title")),
        "body": clean_text(review.get("body")),
    }
