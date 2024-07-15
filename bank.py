import telebot
from telebot import types
import threading
from create_bot import bot, cur2, lock, con2, cursor, con
import menu
import random
import config

def bank(message):
	bank_keyboard = types.InlineKeyboardMarkup()
	but_for_create = types.InlineKeyboardButton(text="Создать чек", callback_data="create_check")
	but_for_clear = types.InlineKeyboardButton(text="Обналичить чек", callback_data="clear_check")
	but_for_menu = types.InlineKeyboardButton(text="Вернуться в меню", callback_data="to_menu")
	bank_keyboard.add(but_for_create, but_for_clear)

	bot.send_message(message.chat.id, "Ты попал в банк, выбери нужный пункт", reply_markup=bank_keyboard)

def bank_callback(call):
	if call.message:
		if call.data == "create_check":
			def create_choice_2(message):
				try:
					clicks = int(message.text)
					data=""
					for i in range(1, 20):
						ch = random.choice(config.letters_for_bank)
						data+=ch
					with lock:
						cursor.execute("SELECT count FROM balance WHERE user_id=?", (message.chat.id,))
						count = cursor.fetchone()
					count = count[0]
					count-=clicks
					if count<0:
						bot.send_message(message.chat.id, "У вас недостаточно средств, возвращаю в меню")
						menu.menu(message)
					else:
						with lock:
							cursor.execute("UPDATE balance SET count=? WHERE user_id=?", (count, message.chat.id))
							con.commit()
						with lock:
							cur2.execute("INSERT INTO checks (user_id, check_id, clicks) VALUES (?, ?, ?)", (message.chat.id, data, clicks))
						bot.send_message(message.chat.id, "Ты создал чек с кодом `"+data+"` для обналичивания введи его в соответсвующем пункте в банке", parse_mode="MarkdownV2")
				except:
					bot.send_message(message.chat.id, "Ты ввёл не число!")
					send = bot.send_message(call.message.chat.id, "Введи сумму чека", reply_markup=bank_keyboard_create)
					bot.register_next_step_handler(send, create_choice_2)

			bank_keyboard_create = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
			but_for_menu = types.KeyboardButton(text="Вернуться в меню")
			bank_keyboard_create.add(but_for_menu)
			send = bot.send_message(call.message.chat.id, "Введи сумму чека", reply_markup=bank_keyboard_create)
			bot.register_next_step_handler(send, create_choice_2)

		elif call.data == "clear_check":
			bot.send_message(call.message.chat.id, "Обналичить чек")
		elif call.data == "to_menu":
			menu.menu(call.message)

def register_handlers(bot: telebot.TeleBot): 
	bot.register_message_handler(bank, commands=['bank'])
	bot.register_callback_query_handler(bank_callback, func=lambda call: True)