import unittest
from scripts.menu_generator import generate_weekly_menu

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

if __name__ == '__main__':
    unittest.main()
