import unittest
import sys
from unittest.mock import patch
from scripts.menu_generator import generate_weekly_menu, write_menu_to_json

class TestMenuGenerator(unittest.TestCase):

    def test_generate_weekly_menu(self):
        # Test if the function returns a dictionary
        menu = generate_weekly_menu()
        self.assertIsInstance(menu, dict)

        # Test if the generated menu contains keys for meal types
        meal_types = ['breakfast', 'lunch', 'dinner']
        for meal_type in meal_types:
            self.assertIn(meal_type, menu)
            self.assertIsInstance(menu[meal_type], list)

        # Test if the generated menu contains the 'week_number' key
        self.assertIn('week_number', menu)
        self.assertIsInstance(menu['week_number'], int)

        # Test if the generated menu contains the 'year' key
        self.assertIn('year', menu)
        self.assertIsInstance(menu['year'], int)

    @patch('menu_generator.open')
    def test_write_menu_to_json(self, mock_open):
        menu = {
            'breakfast': [1, 2, 3],
            'lunch': [4, 5, 6],
            'dinner': [7, 8, 9],
            'week_number': 15,
            'year': 2024
        }

        # Mock the file object
        mock_file = mock_open.return_value.__enter__.return_value

        # Call the function
        write_menu_to_json(menu)

        # Check if the JSON dump method was called with the correct arguments
        mock_file.write.assert_called_once_with(
            '{"breakfast": [1, 2, 3], "lunch": [4, 5, 6], "dinner": [7, 8, 9], "week_number": 15, "year": 2024}')

if __name__ == '__main__':
    unittest.main()
