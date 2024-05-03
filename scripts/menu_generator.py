import sqlite3
from datetime import datetime
import json

# Number of persons
N_PERSONS = 4  #TODO: Make it a variable and be able to be changed in UI
# Number of days
N_DAYS = 7 #TODO: Make it a variable and be able to be changed in UI
# Path to the database
DB_PATH = './data/recipes.db'
# Path to json-file containing the recipe information
JSON_MENU_PATH = './data/weekly_menu.json'

meal_types = ['breakfast', 'lunch', 'dinner']
meal_types_ru = ['Завтрак', 'Обед', 'Ужин']

def lst_to_str(lst: list) -> str:
    """
    Convert a list of elements to a string representation.

    Args:
        lst (list): The list of elements to be converted to a string.

    Returns:
        str: A string representation of the input list with elements enclosed 
             in parentheses and separated by commas.

    Examples:
        >>> lst_to_str([40, 41, 31, 43, 20, 23, 38])
        '(40, 41, 31, 43, 20, 23, 38)'
        >>> lst_to_str(['apple', 'banana', 'cherry'])
        "('apple', 'banana', 'cherry')"
        >>> lst_to_str([])
        '()'

    Note:
        - If the input list is empty, an empty string with parentheses '()' 
          will be returned.
        - Elements in the list will be converted to their string 
          representations using the str() function.
    """
    return '(' + ', '.join(map(str, lst)) + ')'

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
        recipe_ids = [id[0] for id in cursor.execute(query, (N_DAYS,)).fetchall()]
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

MAKE_SHOPPING_LIST = """
SELECT 
    i.ingredient_name, 
    SUM(ri.ingredient_qty) * ? AS total_qty, 
    m.measurement_name 
FROM 
    recipe_ingredients ri
JOIN 
    ingredients i ON ri.ingredient_id = i.ingredient_id
JOIN 
    measurements m ON ri.measurement_id = m.measurement_id
WHERE {}
GROUP BY 
    ri.ingredient_id, m.measurement_name
ORDER BY 
    i.ingredient_name
"""

def make_shopping_list(recipe_ids: list) -> str:
    """
    Uses MAKE_LIST_OF_PRODUCTS query and returns multiple line string 
    of ingredients with their quantities. Makes a list of products to buy.

    Args:
        recipe_ids (list): list of recipe IDs

    Returns:
        str: multiple line string with ingredients and their quantities and 
             measurements
    """
    condition = "ri.recipe_id IN {}".format(lst_to_str(recipe_ids))
    query = MAKE_SHOPPING_LIST.format(condition)

    # Execute the SQL query to retrieve data
    data = cursor.execute(query, (N_PERSONS,)).fetchall()

    # Constructing the string representation of ingredients with their quantities and measurements
    result_str = ""
    for row in data:
        ingredient_name, total_qty, measurement_name = row
        result_str += f"{ingredient_name}: {total_qty} {measurement_name}\n"

    return result_str

MAKE_LIST_OF_DISHES = """
SELECT recipe_name
FROM recipe
WHERE {}
ORDER BY recipe_name
"""

def make_list_of_dishes(recipe_ids: list) -> str:
    """
     Uses MAKE_LIST_OF_DISHES query and returns multiple line string 
    of ingredients with their quantities.  Makes a list of dishes for a week

   Args:
        recipe_ids (list): list of recipe IDs

    Returns:
        str: multiple line string with dishes
    """
    condition = "recipe_id IN {}".format(lst_to_str(recipe_ids))
    query = MAKE_LIST_OF_DISHES.format(condition)

    # Execute the SQL query to retrieve data
    data = cursor.execute(query).fetchall()

    # Constructing the string representation of ingredients with their quantities and measurements
    result_str = ""
    for row in data:
        recipe_name = row[0]
        result_str += f"{recipe_name}\n"

    return result_str


# Initialize SQLite database connection
# TODO: развести процессы формирования menu и отправки сообщений в telegram. Сделать weekly_message_sender.py
with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    print('Generating menu...')  #TODO: писать в логи
    menu = generate_weekly_menu()
    print('Menu generation complete') #TODO: писать в логи

    print('Generating message with dishes list...') #TODO: писать в логи
    msg_recipe_names = ''
    for meal_type, meal_type_ru in zip(meal_types, meal_types_ru):
        msg_recipe_names += meal_type_ru.upper() + '\n'
        msg_recipe_names += make_list_of_dishes(menu[meal_type]) + '\n'
    print('Message generation complete') #TODO: писать в логи

    print('Generating message with buying list...') #TODO: писать в логи
    recipe_ids = []
    for meal_type in meal_types:
        recipe_ids += menu[meal_type]
    msg_shopping_list = make_shopping_list(recipe_ids) + '\n'
    print('Message generation complete') #TODO: писать в логи

print('Sending messages...') #TODO: писать в логи
print('\nСписок блюд')
print(msg_recipe_names) # TODO: send to telegram
print('Список покупок')
print(msg_shopping_list) # TODO: send to telegram
print('Writing recipe IDs to temporary json-file')
write_menu_to_json(menu, path=JSON_MENU_PATH)
print()
