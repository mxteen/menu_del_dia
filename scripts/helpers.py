import json
import requests
from config import SECRETS_PATH

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

def read_menu(path: str):
    # Read menu from JSON file
    with open(path, 'r') as file:
        menu = json.load(file)
    return menu

# TODO: Use invironment variables ang Github Actions instead of secrets.txt
with open (SECRETS_PATH) as f:
    secrets = f.readlines()
# Initializing the bot with the bot token
token = secrets[0].strip()
chat_id = secrets[1].strip()

# TODO: Use python-telegram-bot or aiogram
# Send messages to Telegram
telegram_api_url = f"https://api.telegram.org/bot{token}/sendMessage"

def send_message(text: str) -> None:
    params = {"chat_id": chat_id, "text": text}
    response = requests.post(telegram_api_url, params=params)
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")
