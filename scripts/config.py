# Number of days
N_DAYS = 7 #TODO: Make it a variable and be able to be changed in UI

# Number of persons
N_PERSONS = 4  # TODO: Make it a variable and be able to be changed in UI

# Path to JSON file containing the recipe information
JSON_MENU_PATH = './data/weekly_menu.json'

# Path to the database
DB_PATH = './data/recipes.db'

# Path to secrets.txt # TODO: Use secrets and environment variables instead
SECRETS_PATH = './secrets.txt'

# Path to log-file
LOG_PATH = './logs/menu_del_dia.log'

# Path to excel-file containing recipes
XLSX_PATH = './data/recipes.xlsx'


meal_types = ['breakfast', 'lunch', 'dinner']
meal_types_ru = ['Завтрак', 'Обед', 'Ужин']
days_of_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг',
                'Пятница', 'Суббота', 'Воскресенье']

"""
Another option to share variables across multiple Python files within the same
project is to use environment variables. Environment variables are system-wide
variables that can be accessed by any process running on the system.

Here's how you can use environment variables for your variables.
    1. Set the environment variables in your shell environment (e.g., .bashrc,
    .bash_profile, or .zshrc):

    export N_PERSONS=4
    export JSON_MENU_PATH='./data/weekly_menu.json'
    export DB_PATH='./data/recipes.db'

    2. In Python scripts, access the environment variables using the os.environ
    dictionary:

    import os

    # Get the value of the environment variables
    N_PERSONS = int(os.environ.get('N_PERSONS', 4))
    JSON_MENU_PATH = os.environ.get('JSON_MENU_PATH', './data/weekly_menu.json')
    DB_PATH = os.environ.get('DB_PATH', './data/recipes.db')
"""
