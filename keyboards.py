from telebot.types import (ReplyKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardRemove)

from messages import (BUTTON_START_SHOOTING, BUTTON_CONTINUE_SHOOTING,
                      BUTTON_STOP_SHOOTING, REVERSE_YES, REVERSE_NO)


class BotKeyboard:
    @staticmethod
    def get_keyboard_start_shooting():
        markup = ReplyKeyboardMarkup()
        button = KeyboardButton(BUTTON_START_SHOOTING)
        markup.add(button)
        return markup

    @staticmethod
    def get_keyboard_continue():
        markup = ReplyKeyboardMarkup()
        button_continue = KeyboardButton(BUTTON_CONTINUE_SHOOTING)
        button_stop = KeyboardButton(BUTTON_STOP_SHOOTING)
        markup.add(button_continue)
        markup.add(button_stop)
        return markup

    @staticmethod
    def get_keyboard_reverse():
        markup = ReplyKeyboardMarkup()
        button_yes = KeyboardButton(REVERSE_YES)
        button_no = KeyboardButton(REVERSE_NO)
        markup.add(button_yes)
        markup.add(button_no)
        return markup

    @staticmethod
    def get_empty_keyboard():
        return ReplyKeyboardRemove()
