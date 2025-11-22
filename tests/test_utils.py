"""
Unit tests for utils.py helper functions.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import (
    format_price,
    format_area,
    extract_numbers,
    normalize_text,
    parse_price_from_text,
    parse_area_from_text,
    validate_phone_number,
    format_phone_number,
    extract_property_type,
    calculate_price_per_meter,
    sanitize_input
)


class TestUtils(unittest.TestCase):
    """Tests for helper utilities."""

    def test_format_price(self):
        """Format price in USD-friendly string."""
        self.assertEqual(format_price(5_000_000_000), "$5.00B")
        self.assertEqual(format_price(500_000_000), "$500.00M")
        self.assertEqual(format_price(50_000), "$50,000")
        self.assertEqual(format_price(None), "Unknown")

    def test_format_area(self):
        """Format area with square meter suffix."""
        self.assertEqual(format_area(120.5), "120.5 sq m")
        self.assertEqual(format_area(80), "80.0 sq m")
        self.assertEqual(format_area(None), "Unknown")

    def test_extract_numbers(self):
        """Extract numbers from text (supports Persian digits)."""
        text = "Price 5 billion and area 120 sq m"
        numbers = extract_numbers(text)
        self.assertEqual(len(numbers), 2)
        self.assertIn(5.0, numbers)
        self.assertIn(120.0, numbers)
        
        # Persian digits
        text_persian = "قیمت ۵ میلیارد و متراژ ۱۲۰ متر"
        numbers_persian = extract_numbers(text_persian)
        self.assertEqual(len(numbers_persian), 2)
    
    def test_normalize_text(self):
        """Normalize whitespace and characters."""
        text = "سلام   دنيا  "
        normalized = normalize_text(text)
        self.assertEqual(normalized, "سلام دنیا")
    
    def test_parse_price_from_text(self):
        """Parse numeric price from text."""
        self.assertEqual(parse_price_from_text("Price 5 billion dollars"), 5_000_000_000)
        self.assertEqual(parse_price_from_text("Price 500 million USD"), 500_000_000)
        self.assertEqual(parse_price_from_text("Price about 50 thousand"), 50_000)
    
    def test_parse_area_from_text(self):
        """Parse area value from text."""
        self.assertEqual(parse_area_from_text("120 square meters"), 120.0)
        self.assertEqual(parse_area_from_text("about 80.5 m2"), 80.5)
    
    def test_validate_phone_number(self):
        """Validate phone numbers."""
        self.assertTrue(validate_phone_number("+14155552671"))
        self.assertTrue(validate_phone_number("415-555-2671"))
        self.assertTrue(validate_phone_number("(415) 555-2671"))
        self.assertFalse(validate_phone_number("123456"))
        self.assertFalse(validate_phone_number(None))
    
    def test_format_phone_number(self):
        """Format phone numbers in readable style."""
        self.assertEqual(format_phone_number("4155552671"), "(415) 555-2671")
        self.assertEqual(format_phone_number("+14155552671"), "+1 (415) 555-2671")
    
    def test_extract_property_type(self):
        """Extract property type keywords."""
        self.assertEqual(extract_property_type("Beautiful apartment downtown"), "apartment")
        self.assertEqual(extract_property_type("Modern villa with pool"), "house")
        self.assertEqual(extract_property_type("Large piece of land"), "land")
    
    def test_calculate_price_per_meter(self):
        """Calculate price per square meter."""
        result = calculate_price_per_meter(5000000000, 100)
        self.assertEqual(result, 50000000)
        
        result = calculate_price_per_meter(5000000000, 0)
        self.assertIsNone(result)
    
    def test_sanitize_input(self):
        """Sanitize user inputs."""
        dirty_input = "<script>alert('test')</script>Hello"
        clean = sanitize_input(dirty_input)
        self.assertNotIn("<script>", clean)


if __name__ == '__main__':
    unittest.main()

