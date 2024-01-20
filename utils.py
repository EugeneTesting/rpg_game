import json
from telebot import types

from config import MENU


# Загрузка данных пользователя из файла
def load_user_data():
    with open("user_data.json", "r") as file:
        return json.load(file)


# Сохранение данных пользователя в файл
def save_user_data(user_data):
    with open("user_data.json", "w") as file:
        json.dump(user_data, file)


# Загрузка локаций из файла
def load_locations():
    with open("locations.json", "r", encoding='utf-8') as file:
        return json.load(file)


# Получаем основное меню
def get_menu_keyboard():
    menu_keyboard = types.ReplyKeyboardMarkup(row_width=3,
                                              resize_keyboard=True,
                                              one_time_keyboard=True)
    menu_keyboard.add(*MENU.keys())
    return menu_keyboard


# Получаем меню с кнопками из словаря
def get_keyboard_from_actions(actions):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for action_text, action_command in actions.items():
        keyboard.add(types.KeyboardButton(action_text))
    return keyboard


# Получаем текущую локацию
def get_current_location(obj_data, user_id):
    current_location = obj_data.get(user_id, {}).get(
        'current_location', 'start')
    return current_location
