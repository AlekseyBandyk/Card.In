import telebot
from telebot import types
from create_bot import bot

def menu(message):
	menu_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
	but_for_click = types.KeyboardButton('Кликать')
	but_for_profile = types.KeyboardButton('Профиль')
	but_for_mg = types.KeyboardButton('Мини-игры')
	but_for_quests = types.KeyboardButton("Квесты")
	but_for_trade = types.KeyboardButton("Торговая площадка")
	but_for_ask = types.KeyboardButton("Обратная связь")
	menu_keyboard.add(but_for_click, but_for_profile, but_for_mg, but_for_quests, but_for_trade, but_for_ask)
	bot.send_message(message.chat.id, "Меню", reply_markup=menu_keyboard)

def register_handlers(bot: telebot.TeleBot):
	bot.register_message_handler(menu, commands=['menu'])