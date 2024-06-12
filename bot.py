import telebot

from config import TOKEN
from graph import get_graph
from keyboards import BotKeyboard
from messages import WELCOME, BUTTON_START_SHOOTING, PRESSURE_SAVE_START, \
    PRESSURE_ERROR, SPEED_SAVE_START, SPEED_ERROR, SAVE_SUCCESS, \
    BUTTON_CONTINUE_SHOOTING, BUTTON_STOP_SHOOTING, ERROR_CHOOSE_ACTION, \
    REVERSE_GRAPH, REVERSE_YES, GRAPH_START, GRAPH_END

bot = telebot.TeleBot(TOKEN)

keyboards = BotKeyboard()

SHOOT_DATA = {}


@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    with open('graphs/base_graph.png', 'rb') as file:
        file_data = file.read()
    bot.send_message(chat_id,
                     WELCOME,
                     reply_markup=keyboards.get_keyboard_start_shooting())
    bot.send_photo(chat_id, file_data)


@bot.message_handler(
    func=lambda message: message.text == BUTTON_START_SHOOTING
)
def start_shoot(message):
    chat_id = message.chat.id
    SHOOT_DATA[chat_id] = {}
    bot.send_message(chat_id,
                     'Вы начали пристрелку!',
                     reply_markup=keyboards.get_empty_keyboard())
    send_pressure(message)


def send_pressure(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     PRESSURE_SAVE_START,
                     reply_markup=keyboards.get_empty_keyboard())
    bot.register_next_step_handler(message, save_pressure)


def save_pressure(message):
    pressure: str = message.text
    chat_id = message.chat.id
    if not pressure.isdigit():
        bot.send_message(PRESSURE_ERROR)
        send_pressure(message)
        return
    SHOOT_DATA[chat_id][int(pressure)] = None
    send_speed(message)


def send_speed(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, SPEED_SAVE_START)
    bot.register_next_step_handler(message, save_speed)


def save_speed(message):
    speed: str = message.text
    chat_id = message.chat.id
    if not speed.replace('.', '', 1).isdigit():
        bot.send_message(chat_id, SPEED_ERROR)
        send_pressure(message)
        return
    for i in SHOOT_DATA[chat_id]:
        if SHOOT_DATA[chat_id][i] is None:
            SHOOT_DATA[chat_id][i] = float(speed)
    bot.send_message(chat_id,
                     SAVE_SUCCESS,
                     reply_markup=keyboards.get_keyboard_continue())
    bot.register_next_step_handler(message, choose_action)


def choose_action(message):
    chat_id = message.chat.id
    text = message.text
    if text == BUTTON_CONTINUE_SHOOTING:
        send_pressure(message)
    elif text == BUTTON_STOP_SHOOTING:
        send_graph_start(message)
    else:
        bot.send_message(chat_id,
                         ERROR_CHOOSE_ACTION,
                         reply_markup=keyboards.get_keyboard_continue())
        bot.register_next_step_handler(message, choose_action)


def send_graph_start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     REVERSE_GRAPH,
                     reply_markup=keyboards.get_keyboard_reverse())
    bot.register_next_step_handler(message, send_graph_end)


def send_graph_end(message):
    chat_id = message.chat.id
    status = True if message.text == REVERSE_YES else False
    bot.send_message(chat_id,
                     GRAPH_START,
                     reply_markup=keyboards.get_empty_keyboard())
    print(SHOOT_DATA[chat_id])
    img_path = get_graph(SHOOT_DATA[chat_id], status)
    bot.send_message(chat_id,
                     GRAPH_END)
    with open(f'graphs/{img_path}', 'rb') as file:
        file_data = file.read()
    SHOOT_DATA[chat_id] = {}
    bot.send_photo(chat_id, file_data,
                   reply_markup=keyboards.get_keyboard_start_shooting())
