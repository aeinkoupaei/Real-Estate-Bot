"""
Unit tests for database.py
"""
import unittest
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import DatabaseManager, Property


class TestDatabaseManager(unittest.TestCase):
    """Tests for DatabaseManager"""
    
    def setUp(self):
        """Create a fresh in-memory database before each test"""
        self.db = DatabaseManager('sqlite:///:memory:')
        
        # Sample property data
        self.sample_property = {
            'title': 'Sample Apartment',
            'property_type': 'apartment',
            'city': 'Tehran',
            'neighborhood': 'Valiasr',
            'address': 'Valiasr Street, No. 123',
            'area': 120.5,
            'rooms': 2,
            'floor': 3,
            'year_built': 2019,
            'price': 5_000_000_000,
            'parking': True,
            'elevator': True,
            'storage': False,
            'description': 'A beautiful modern apartment'
        }
    
    def test_add_property(self):
        """Adding a property should return an integer ID"""
        property_id = self.db.add_property(123456, self.sample_property)
        self.assertIsNotNone(property_id)
        self.assertIsInstance(property_id, int)
    
    def test_get_property(self):
        """Verify a stored property can be retrieved"""
        property_id = self.db.add_property(123456, self.sample_property)
        property_obj = self.db.get_property(property_id)
        
        self.assertIsNotNone(property_obj)
        self.assertEqual(property_obj.title, 'Sample Apartment')
        self.assertEqual(property_obj.city, 'Tehran')
        self.assertEqual(property_obj.area, 120.5)
    
    def test_get_user_properties(self):
        """Return all properties belonging to a user"""
        user_id = 123456
        
        self.db.add_property(user_id, self.sample_property)
        
        property2 = self.sample_property.copy()
        property2['title'] = 'Second Property'
        self.db.add_property(user_id, property2)
        
        properties = self.db.get_user_properties(user_id)
        
        self.assertEqual(len(properties), 2)
    
    def test_search_properties(self):
        """Search should respect filters"""
        self.db.add_property(123456, self.sample_property)
        
        property2 = self.sample_property.copy()
        property2['city'] = 'Isfahan'
        property2['price'] = 3_000_000_000
        self.db.add_property(123457, property2)
        
        results = self.db.search_properties({'city': 'Tehran'})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].city, 'Tehran')
        
        results = self.db.search_properties({
            'min_price': 2_000_000_000,
            'max_price': 4_000_000_000
        })
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].price, 3_000_000_000)
    
    def test_update_property(self):
        """Updates should persist"""
        property_id = self.db.add_property(123456, self.sample_property)
        
        updates = {'price': 6_000_000_000, 'rooms': 3}
        result = self.db.update_property(property_id, updates)
        
        self.assertTrue(result)
        
        property_obj = self.db.get_property(property_id)
        self.assertEqual(property_obj.price, 6_000_000_000)
        self.assertEqual(property_obj.rooms, 3)
    
    def test_delete_property(self):
        """Deleting should remove the record"""
        user_id = 123456
        property_id = self.db.add_property(user_id, self.sample_property)
        
        result = self.db.delete_property(property_id, user_id)
        self.assertTrue(result)
        
        property_obj = self.db.get_property(property_id)
        self.assertIsNone(property_obj)
    
    def test_statistics(self):
        """get_statistics returns totals and averages"""
        self.db.add_property(123456, self.sample_property)
        
        property2 = self.sample_property.copy()
        property2['area'] = 80
        property2['price'] = 3_000_000_000
        self.db.add_property(123457, property2)
        
        stats = self.db.get_statistics()
        
        self.assertEqual(stats['total_properties'], 2)
        self.assertGreater(stats['average_price'], 0)
        self.assertGreater(stats['average_area'], 0)
    
    def test_property_to_dict(self):
        """Property.to_dict should return a dictionary"""
        property_id = self.db.add_property(123456, self.sample_property)
        property_obj = self.db.get_property(property_id)
        
        property_dict = property_obj.to_dict()
        
        self.assertIsInstance(property_dict, dict)
        self.assertEqual(property_dict['title'], 'Sample Apartment')
        self.assertEqual(property_dict['city'], 'Tehran')
    
    def test_property_to_text(self):
        """Property.to_text should return readable text"""
        property_id = self.db.add_property(123456, self.sample_property)
        property_obj = self.db.get_property(property_id)
        
        text = property_obj.to_text()
        
        self.assertIsInstance(text, str)
        self.assertIn('Sample Apartment', text)
        self.assertIn('Tehran', text)


if __name__ == '__main__':
    unittest.main()

