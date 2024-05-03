import os
import sqlite3
from datetime import datetime, timedelta
import json
from helpers import lst_to_str
from config import JSON_MENU_PATH, DB_PATH, N_DAYS, meal_types

# Define SQLite query
GET_RANDOM_RECIPES = """
SELECT r.recipe_id
FROM recipe r
JOIN meal_type m ON r.meal_type_id = m.meal_type_id
WHERE {}
ORDER BY RANDOM() LIMIT ?
"""

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
    where_conditions = [
        "m.meal_type_name = 'Завтрак'",
        "m.meal_type_name = 'Обед или ужин'",
        "m.meal_type_name = 'Обед или ужин'" +\
              f"AND r.recipe_id NOT IN {lst_to_str(recipe_ids)}"
    ]

    for meal_type, condition in zip(meal_types, where_conditions):
        # Execute SQL query to fetch random recipe IDs
        query = GET_RANDOM_RECIPES.format(condition)
        # Fetch recipe_ids and extract IDs from tuples
        recipe_ids = [
            id[0] for id in cursor.execute(query, (N_DAYS,)).fetchall()]
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
        path (str): Optional. The path to the JSON file. Default is 
                    'weekly_menu.json'.

    Example usage:
        write_menu_to_json(menu, 'menu.json')
    """
    with open(path, 'w') as file:
        json.dump(menu, file, indent=4)

# Check if weekly menu file exists and is up to date
def is_weekly_menu_up_to_date():
    """
    Check if the weekly menu file exists and is up to date.

    This function checks if the weekly menu file exists at the specified path
    (JSON_MENU_PATH) and if it was modified within the last 7 days. If the file
    does not exist or if it is older than 7 days, the function returns False,
    indicating that the menu is not up to date. Otherwise, it returns True.

    Returns:
        bool: True if the weekly menu file exists and was modified within the
              last 7 days, False otherwise.
    """
    if not os.path.exists(JSON_MENU_PATH):
        return False
    else:
        last_modified_time = os.path.getmtime(JSON_MENU_PATH)
        last_modified_date = datetime.fromtimestamp(last_modified_time).date()
        current_date = datetime.now().date()
        return (current_date - last_modified_date) <= timedelta(days=7)

if not is_weekly_menu_up_to_date():
    # Initialize SQLite database connection
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        print('Generating menu...')  #TODO: писать в логи
        menu = generate_weekly_menu()
        print('Menu generation complete') #TODO: писать в логи
    print('Writing recipe IDs to temporary json-file')
    write_menu_to_json(menu, path=JSON_MENU_PATH)
else:
    print('The menu is up to date')
