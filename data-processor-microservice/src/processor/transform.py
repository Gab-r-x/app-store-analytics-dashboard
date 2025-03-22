import re
import unicodedata

def transform_app_data(app_data):
    """Apply transformations to normalized app data."""
    transformed = app_data.copy()

    # Clean text fields
    for field in ["name", "subtitle", "developer", "description", "rating_summary"]:
        if transformed.get(field):
            transformed[field] = clean_text(transformed[field])

    # Clean reviews
    if transformed.get("reviews"):
        transformed["reviews"] = [clean_review(r) for r in transformed["reviews"]]

    # Clean general info keys/values
    if transformed.get("general_info"):
        transformed["general_info"] = {
            clean_text(k): clean_text(v) for k, v in transformed["general_info"].items()
        }

    return transformed

def clean_text(text):
    """Normalize and clean string data."""
    if not isinstance(text, str):
        return text
    text = unicodedata.normalize("NFKC", text)
    text = text.encode("utf-8", errors="ignore").decode("utf-8")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_review(review):
    """Clean each field inside a review dict."""
    return {
        "rating": clean_text(review.get("rating")),
        "author": clean_text(review.get("author")),
        "date": clean_text(review.get("date")),
        "title": clean_text(review.get("title")),
        "body": clean_text(review.get("body")),
    }
