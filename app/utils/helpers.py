import secrets
import re


def generate_invite_code(length: int = 8) -> str:
    """Generate a random uppercase invite code, e.g. 'AX7KPQ2R'."""
    return secrets.token_urlsafe(length)[:length].upper()


def slugify(text: str) -> str:
    """
    Convert a challenge title to a URL-safe slug.

    Example:
        slugify("Two Sum") -> "two-sum"
        slugify("Valid Parentheses!") -> "valid-parentheses"
    """
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)      # remove non-word chars
    text = re.sub(r"[\s_]+", "-", text)        # spaces/underscores -> hyphens
    text = re.sub(r"-+", "-", text)            # collapse multiple hyphens
    return text


def success_response(data=None, message=None, status=200):
    """Return a standardised success JSON dict."""
    response = {"success": True}
    if message:
        response["message"] = message
    if data is not None:
        response["data"] = data
    return response, status


def error_response(message: str, status: int = 400):
    """Return a standardised error JSON dict."""
    return {"success": False, "error": message}, status
