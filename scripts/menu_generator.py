import sqlite3
from datetime import datetime
import json
import os

# Path to the database
DB_PATH = '../data/recipes.db'
# Path to json-file containing the recipe information
JSON_MENU_PATH = '../data/weekly_menu.json'

# Define SQLite query
GET_RANDOM_RECIPES = """
SELECT r.recipe_id
FROM recipe r
JOIN meal_type m ON r.meal_type_id = m.meal_type_id
WHERE {}
ORDER BY RANDOM() LIMIT ?
"""

def lst_to_str(lst: list) -> str:
    """
    Convert a list of elements to a string representation.

    Args:
        lst (list): The list of elements to be converted to a string.

    Returns:
        str: A string representation of the input list with elements enclosed in parentheses
             and separated by commas.

    Examples:
        >>> lst_to_str([40, 41, 31, 43, 20, 23, 38])
        '(40, 41, 31, 43, 20, 23, 38)'
        >>> lst_to_str(['apple', 'banana', 'cherry'])
        "('apple', 'banana', 'cherry')"
        >>> lst_to_str([])
        '()'

    Note:
        - If the input list is empty, an empty string with parentheses '()' will be returned.
        - Elements in the list will be converted to their string representations using the str() function.
    """
    return '(' + ', '.join(map(str, lst)) + ')'

def generate_weekly_menu():
    """
    Generate a weekly menu by selecting random recipes for each meal type.

    This function queries the database to retrieve random recipe IDs for each
    meal type (breakfast, lunch, and dinner) based on specified conditions.
    The conditions ensure that for breakfast, only breakfast recipes are
    selected, while for lunch and dinner, recipes can be chosen from a broader
    category. Additionally, dinner recipes that have already been selected for
    lunch in the week are excluded.

    Returns:
        dict: A dictionary containing meal types as keys and lists of recipe
              IDs as values. Each list represents the selected recipes for
              the corresponding meal type. The dictionary also includes a
              'week_number' key, indicating the number of the current week
              in the year, and a 'year' key, indicating the current year.


    Example usage:
        menu = generate_weekly_menu()
        print(menu)
    """
    menu = dict()
    recipe_ids = list()
    # Meal types and corresponding conditions
    meal_types = ['breakfast', 'lunch', 'dinner']
    where_conditions = [
        "m.meal_type_name = 'Завтрак'",
        "m.meal_type_name = 'Обед или ужин'",
        f"m.meal_type_name = 'Обед или ужин' AND r.recipe_id NOT IN {lst_to_str(recipe_ids)}" 
    ]

    for meal_type, condition in zip(meal_types, where_conditions):
        # Execute SQL query to fetch random recipe IDs
        query = GET_RANDOM_RECIPES.format(condition)
        # Fetch recipe_ids and extract IDs from tuples
        recipe_ids = [id[0] for id in cursor.execute(query, (7,)).fetchall()]
        # Store the selected recipe IDs for the current meal type
        menu[meal_type] = recipe_ids

    # Get the current week number and year
    current_date = datetime.now()
    week_number = current_date.isocalendar()[1]
    year = current_date.year

    # Add week number and year to the menu dictionary
    menu['week_number'] = week_number
    menu['year'] = year
    # TODO: Add user Id to the output dictionary

    return menu


# Function to write menu to JSON file
def write_menu_to_json(menu, path='weekly_menu.json'):
    """
    Write the menu dictionary to a JSON file.

    Args:
        menu (dict): A dictionary containing the menu data.
        path (str): Optional. The path to the JSON file. Default is 'weekly_menu.json'.

    Example usage:
        write_menu_to_json(menu, 'menu.json')
    """
    with open(path, 'w') as file:
        json.dump(menu, file, indent=4)


# Initialize SQLite database connection
with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    menu = generate_weekly_menu()

write_menu_to_json(menu, path=JSON_MENU_PATH)
