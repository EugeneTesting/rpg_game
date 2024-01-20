import telebot
from telebot import types

from utils import (load_locations, get_menu_keyboard,
                   get_keyboard_from_actions, get_current_location,
                   load_user_data, save_user_data)
from config import TOKEN, MENU

# Загружаем данные пользователя
try:
    user_data = load_user_data()
except:
    user_data = {}

# Загружаем локации
try:
    locations = load_locations()
except FileNotFoundError:
    print(f'Проверьте, что файл существует.')
    raise

# Инициализируем бота
bot = telebot.TeleBot(TOKEN)
bot.set_my_commands(
    commands=[types.BotCommand(command, description) for command, description
              in MENU.items()])


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.from_user.id, '''
/start - Начать
/help - Помощь''', reply_markup=get_menu_keyboard())


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Определяем начальную локацию
    current_location = get_current_location(user_data,
                                            str(message.from_user.id))
    # Отправляем её пользователю
    send_location_description(message, current_location)


# Обработчик получения сообщения
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Обрабатываем условие 'Выйти из игры'
    if message.text == 'Выйти из игры':
        if str(message.from_user.id) in user_data:
            del user_data[str(message.from_user.id)]
            save_user_data(user_data)

        bot.send_message(
            message.chat.id,
            "Спасибо за игру!", reply_markup=types.ReplyKeyboardRemove()
        )
        return

    # Проверяем, что пользователь начал анкету
    if str(message.chat.id) not in user_data:
        bot.send_message(
            message.chat.id,
            "Пожалуйста, начните анкету с помощью команды /start",
        )
        return

    try:
        # Если нет ошибок в данных и есть ключ в словаре
        current_location = get_current_location(user_data,
                                                str(message.from_user.id))
        next_location = locations['locations'][current_location]['actions'][
            message.text]
        send_location_description(message, next_location)
    except KeyError:
        bot.send_message(
            message.chat.id,
            "Пожалуйста, начните анкету с помощью команды /start",
        )


# Отправляем пользователю картинку, описание локации и кнопки для действий
def send_location_description(message, location_key):
    location = locations['locations'][location_key]
    description = location['description']
    actions = location.get('actions', {})
    image = location.get('image')

    if image:
        bot.send_photo(message.chat.id, open(image, 'rb'))
    bot.send_message(message.from_user.id, description,
                     reply_markup=get_keyboard_from_actions(actions))

    # Обновляем данные пользователя с текущей локацией
    user_data[str(message.from_user.id)] = {'current_location': location_key}

    # Сохраняем обновленные данные пользователя
    save_user_data(user_data)


# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
