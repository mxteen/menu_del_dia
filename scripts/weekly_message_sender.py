import sqlite3
import logging
from helpers import lst_to_str, read_menu, send_message
from config import JSON_MENU_PATH, DB_PATH, N_PERSONS, LOG_PATH
from config import meal_types, meal_types_ru

# Set up logging with append mode
logging.basicConfig(filename=LOG_PATH, level=logging.INFO,
                    filemode='a')

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

menu = read_menu(JSON_MENU_PATH)
# Initialize SQLite database connection
with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    logging.info('Generating message with dishes list...')
    msg_recipe_names = ''
    for meal_type, meal_type_ru in zip(meal_types, meal_types_ru):
        msg_recipe_names += meal_type_ru.upper() + '\n'
        msg_recipe_names += make_list_of_dishes(menu[meal_type]) + '\n'
    logging.info('Message generation complete')

    logging.info('Generating message with shopping list...')
    recipe_ids = []
    for meal_type in meal_types:
        recipe_ids += menu[meal_type]
    msg_shopping_list = make_shopping_list(recipe_ids) + '\n'
    logging.info('Message generation complete')

logging.info('Sending messages...')
send_message('Список блюд:\n' + msg_recipe_names)
send_message('Список покупок:\n' + msg_shopping_list)
logging.info('Messages sent to Telegram.')
