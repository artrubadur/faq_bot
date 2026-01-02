def validate_page(page: str):
    if not page.isdigit():
        raise ValueError("Page is invalid")

    if int(page) < 1:
        raise ValueError("Page cannot be less than one")

    return page
