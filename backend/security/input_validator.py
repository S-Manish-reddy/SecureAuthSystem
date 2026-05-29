import bleach


def sanitize_input(user_input: str):

    cleaned_input = bleach.clean(
        user_input,
        tags=[],
        strip=True
    )

    return cleaned_input