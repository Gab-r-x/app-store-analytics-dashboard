def validate_app_data(app_data):
    """
    Validates the transformed app data before insertion into PostgreSQL.
    Returns True if valid, otherwise raises ValueError with explanation.
    """
    required_fields = [
        "apple_id", "name", "developer", "url", "category", "rank"
    ]

    for field in required_fields:
        if not app_data.get(field):
            raise ValueError(f"Missing required field: {field}")

    if not isinstance(app_data["rank"], int):
        raise ValueError("Field 'rank' must be an integer")

    for num_field in ["monthly_downloads_estimate", "monthly_revenue_estimate"]:
        if num_field in app_data and app_data[num_field] is not None:
            if not isinstance(app_data[num_field], (int, float)):
                raise ValueError(f"Field '{num_field}' must be a number")

    for list_field in ["screenshots", "privacy_data", "labels"]:
        if app_data.get(list_field) is not None and not isinstance(app_data[list_field], list):
            raise ValueError(f"Field '{list_field}' must be a list")

    for json_field in ["reviews", "general_info"]:
        if app_data.get(json_field) is not None and not isinstance(app_data[json_field], (dict, list)):
            raise ValueError(f"Field '{json_field}' must be a dict or list")

    return True
