import sqlite3
from datetime import datetime
from config import JSON_MENU_PATH, DB_PATH, N_PERSONS
from config import meal_types, meal_types_ru, days_of_week
from helpers import lst_to_str, read_menu

# Get the menu dictionary
menu = read_menu(JSON_MENU_PATH)
# Get the current day number
# -1 because Sunday is Sunday is 0, Monday is 1... To make Monday 0 we need to subtract 1.
# +1 We need to send the recipe one day before.
current_day_number = datetime.now().isocalendar()[2] # -1+1

# print(menu)
print(current_day_number)

GET_RECIPE_NAME = """
SELECT recipe_name
FROM recipe
WHERE {}
"""

GET_RECIPE_STEPS = """
SELECT recipe_steps
FROM recipe
WHERE {}
"""

GET_INGRGREDIENTS = """
SELECT ingredient_name, ingredient_qty * ?, measurement_name
FROM recipe_ingredients ri 
JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
JOIN measurements m ON ri.measurement_id = m.measurement_id
WHERE {}
"""

def make_menu_for_the_day(menu: dict, day_number: int, meal_type: str) -> str:
    """
    Generates the menu for the day. Uses the day_number and GET_RECIPE_NAME,
    GET_RECIPE_STEPS, GET_INGRGREDIENTS SQL-queries.

    Args:
        day_number (int): _description_
        menu (dict): _description_
        meal_type (str): _description_
        recipe_id (int): _description_

    Returns:
        str: the message containing the meal type (breakfast, dinner ...),
        recipe name for the meal of the day, list of ingredients and 
        preparation description.
    
    Example:
        Понедельник

        ЗАВТРАК

        Салат ABCD
        Ингрединеты:
        ▪ ингредиент A - w г.
        ▪ ингредиент B - x г.
        ▪ ингредиент C - y г.
        ▪ ингредиент D - z мл.

        Рецепт
        Взять A, B и C, порезать и смешать. Залить D. 
        Посолить, поперчить, разложить по тарелкам.

    """
    recipe_id = menu[meal_type][day_number]

    # Constructing the message with recipe name, its' ingredients and their
    # quantities and measurements.
    condition = f"recipe_id = {recipe_id}"
    # Execute the SQL queries to retrieve data
    # Adding recipe name 
    query_name = GET_RECIPE_NAME.format(condition)
    data_name = cursor.execute(query_name).fetchall()
    result_str = data_name[0][0] + '\n'
    # print(result_str, type(result_str))
    # Adding recipe ingredients
    query_ingredients = GET_INGRGREDIENTS.format(condition)
    data_ingredients = cursor.execute(
        query_ingredients, (N_PERSONS,)).fetchall()
    for row in data_ingredients:
        ingredient_name, total_qty, measurement_name = row
        result_str += f"▪ {ingredient_name} - {total_qty} {measurement_name}\n"
    # Adding recipe preparation steps
    query_steps = GET_RECIPE_STEPS.format(condition)
    data_steps = cursor.execute(query_steps).fetchall()
    result_str += data_steps[0][0]
    return result_str

print(f'Generating messages with recipes for the day {current_day_number}...') #TODO: писать в логи
messages = []
# Initialize SQLite database connection
with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    for meal_type, meal_type_ru in zip(meal_types, meal_types_ru):
        msg = f"{days_of_week[current_day_number].upper()}. "
        msg += meal_type_ru.upper() + '\n'
        msg += make_menu_for_the_day(
            menu=menu, day_number=current_day_number, meal_type=meal_type) + '\n'
        messages.append(msg)
print('Messages generation complete') #TODO: писать в логи

for msg in messages: print(msg)
