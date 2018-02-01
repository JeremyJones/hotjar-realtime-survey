from validate_email import validate_email

def valid_email(email: str) -> bool:
    """
    Email verification is a wrapper for the validate_email module.
    Defaults to syntax-only.
    """
    return validate_email(email)
