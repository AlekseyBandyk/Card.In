import telebot
from telebot import types
from create_bot import bot

def click(message):
	click_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
	click_button = types.KeyboardButton('Click!')
	but_for_menu = types.KeyboardButton("Вернуться в меню")
	click_keyboard.add(click_button, but_for_menu)
	bot.send_message(message.chat.id, "Нажмите на кнопку для клика", reply_markup=click_keyboard)

def register_handlers(bot: telebot.TeleBot):
	bot.register_message_handler(click, commands=["click"])