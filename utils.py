"""
Utility helpers for formatting, parsing, and sanitizing user input.
"""
import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def format_price(price):
    """
    Format a numeric price into a readable US dollar string.

    Args:
        price (float|int|str): Price value.

    Returns:
        str: Formatted price string.
    """
    if price is None or price == "":
        return "Unknown"

    try:
        price = float(price)

        if price >= 1_000_000_000:
            return f"${price / 1_000_000_000:.2f}B"
        if price >= 1_000_000:
            return f"${price / 1_000_000:.2f}M"
        if price >= 1_000:
            return f"${price:,.0f}"
        return f"${price:,.0f}"
    except (ValueError, TypeError):
        return str(price)


def format_area(area):
    """
    Format area values and append square meters label.

    Args:
        area (float|int|str): Area size.

    Returns:
        str: Formatted area string.
    """
    if area is None or area == "":
        return "Unknown"

    try:
        return f"{float(area):,.1f} sq m"
    except (ValueError, TypeError):
        return str(area)


def extract_numbers(text):
    """
    Extract numeric values from a string (supports Persian digits).

    Args:
        text (str): Input text.

    Returns:
        list[float]: List of extracted numbers.
    """
    persian_to_english = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
    text = text.translate(persian_to_english)

    numbers = re.findall(r'\d+(?:\.\d+)?', text)
    return [float(n) for n in numbers]


def normalize_text(text):
    """
    Normalize user-provided text by unifying characters and whitespace.

    Args:
        text (str): Input text.

    Returns:
        str: Normalized text.
    """
    if not text:
        return ""

    text = text.replace('ك', 'ک').replace('ي', 'ی')
    text = ' '.join(text.split())

    return text.strip()


def parse_price_from_text(text):
    """
    Extract a numeric price mention from text (supports English & Persian words).

    Args:
        text (str): Input string containing a price phrase.

    Returns:
        float|None: Price in base currency (USD) or None if not detected.
    """
    if not text:
        return None

    text = text.lower()
    numbers = extract_numbers(text)

    if not numbers:
        return None

    price = numbers[0]

    billion_keywords = ['billion', 'billions', 'میلیارد']
    million_keywords = ['million', 'millions', 'میلیون']
    thousand_keywords = ['thousand', 'thousands', 'هزار', 'k']

    if any(word in text for word in billion_keywords):
        price *= 1_000_000_000
    elif any(word in text for word in million_keywords):
        price *= 1_000_000
    elif any(word in text for word in thousand_keywords):
        price *= 1_000

    return price


def parse_area_from_text(text):
    """
    Extract area (in square meters) from text.

    Args:
        text (str): Input text.

    Returns:
        float|None: Area value or None if missing.
    """
    numbers = extract_numbers(text)

    if not numbers:
        return None

    return numbers[0]


def validate_phone_number(phone):
    """
    Validate international phone numbers (E.164 style).

    Args:
        phone (str): Phone number.

    Returns:
        bool: True if phone looks valid.
    """
    if not phone:
        return False

    phone = re.sub(r'\D', '', phone)

    return 7 <= len(phone) <= 15


def format_phone_number(phone):
    """
    Format a phone number into a readable style.

    Args:
        phone (str): Raw phone string.

    Returns:
        str: Formatted number.
    """
    if not phone:
        return ""

    phone = re.sub(r'\D', '', phone)

    if len(phone) == 10:
        return f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"

    if len(phone) == 11 and phone.startswith('1'):
        return f"+1 ({phone[1:4]}) {phone[4:7]}-{phone[7:]}"

    if len(phone) > 4:
        return f"+{phone[:-7]} {phone[-7:-4]}-{phone[-4:]}"

    return phone


def get_persian_date(date_obj=None):
    """
    Return a YYYY/MM/DD formatted date string.

    Args:
        date_obj (datetime): Optional datetime object.

    Returns:
        str: Date string.
    """
    if not date_obj:
        date_obj = datetime.now()

    return date_obj.strftime('%Y/%m/%d')


def truncate_text(text, max_length=100, suffix='...'):
    """
    Shorten text while keeping readability.

    Args:
        text (str): Input text.
        max_length (int): Max allowed length.
        suffix (str): Suffix to append when truncated.

    Returns:
        str: Shortened text.
    """
    if not text or len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)].strip() + suffix


def extract_property_type(text):
    """
    Detect property type keywords within text.

    Args:
        text (str): Input text.

    Returns:
        str|None: Property type label.
    """
    text = text.lower()

    property_types = {
        'apartment': ['apartment', 'condo', 'flat', 'unit'],
        'house': ['house', 'home', 'villa', 'detached'],
        'land': ['land', 'lot', 'parcel'],
        'shop': ['shop', 'store', 'retail'],
        'office': ['office', 'workspace'],
        'suite': ['suite', 'studio']
    }

    for prop_type, keywords in property_types.items():
        for keyword in keywords:
            if keyword in text:
                return prop_type

    return None


def calculate_price_per_meter(price, area):
    """
    Calculate price per square meter.

    Args:
        price (float|int): Total price.
        area (float|int): Property size.

    Returns:
        float|None: Price per square meter.
    """
    try:
        if area and float(area) > 0:
            return float(price) / float(area)
    except (ValueError, TypeError, ZeroDivisionError):
        return None

    return None


def log_user_action(user_id, action, details=""):
    """
    Log user actions for debugging / analytics.

    Args:
        user_id (int|str): User identifier.
        action (str): Action label.
        details (str): Additional details.
    """
    logger.info("User %s - Action: %s - Details: %s", user_id, action, details)


def sanitize_input(text, max_length=1000):
    """
    Remove potentially harmful characters and enforce max length.

    Args:
        text (str): User input.
        max_length (int): Maximum allowed length.

    Returns:
        str: Sanitized text.
    """
    if not text:
        return ""

    text = text[:max_length]
    text = text.replace('<script>', '').replace('</script>', '')
    text = normalize_text(text)

    return text


class PropertyFilter:
    """Helper builder for property search filters."""

    def __init__(self):
        self.filters = {}

    def add_price_range(self, min_price=None, max_price=None):
        """Add price range filter."""
        if min_price is not None:
            self.filters['min_price'] = min_price
        if max_price is not None:
            self.filters['max_price'] = max_price
        return self

    def add_area_range(self, min_area=None, max_area=None):
        """Add area range filter."""
        if min_area is not None:
            self.filters['min_area'] = min_area
        if max_area is not None:
            self.filters['max_area'] = max_area
        return self

    def add_location(self, city=None, neighborhood=None):
        """Add city/neighborhood filters."""
        if city:
            self.filters['city'] = city
        if neighborhood:
            self.filters['neighborhood'] = neighborhood
        return self

    def add_property_type(self, property_type):
        """Add property type filter."""
        if property_type:
            self.filters['property_type'] = property_type
        return self

    def add_rooms(self, rooms):
        """Add room count filter."""
        if rooms is not None:
            self.filters['rooms'] = rooms
        return self

    def add_amenities(self, parking=None, elevator=None, storage=None):
        """Add amenity filters."""
        if parking is not None:
            self.filters['parking'] = parking
        if elevator is not None:
            self.filters['elevator'] = elevator
        if storage is not None:
            self.filters['storage'] = storage
        return self

    def get_filters(self):
        """Return the compiled filter dict."""
        return self.filters

    def clear(self):
        """Clear all filters."""
        self.filters = {}
        return self

