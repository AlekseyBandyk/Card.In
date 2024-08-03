import telebot
from telebot import types
import threading
from create_bot import bot, cur2, lock, con2, cursor, con, write_to_admin
import menu
import random
import config

def bank(message):
	bank_keyboard = types.InlineKeyboardMarkup()
	but_for_create = types.InlineKeyboardButton(text="Создать чек", callback_data="create_check")
	but_for_clear = types.InlineKeyboardButton(text="Обналичить чек", callback_data="clear_check")
	but_for_menu = types.InlineKeyboardButton(text="Вернуться в меню", callback_data="to_menu")
	bank_keyboard.add(but_for_create, but_for_clear, but_for_menu)
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
						write_to_admin()
					count = count[0]
					count-=clicks
					if count<0:
						bot.send_message(message.chat.id, "У вас недостаточно средств, возвращаю в меню")
						menu.menu(message)
					else:
						with lock:
							cursor.execute("UPDATE balance SET count=? WHERE user_id=?", (count, message.chat.id))
							con.commit()
							write_to_admin()
						with lock:
							cur2.execute("INSERT INTO checks (user_id, check_id, clicks) VALUES (?, ?, ?)", (message.chat.id, data, clicks))
							write_to_admin()
						bot.send_message(message.chat.id, "Ты создал чек с кодом `"+data+"` для обналичивания введи его в соответсвующем пункте в банке", parse_mode="MarkdownV2")
						menu.menu(message)
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
			def clear_true(message):
				if message.text == "Вернуться в меню":
					menu.menu(message)
				else:
					with lock:
						cur2.execute("SELECT check_id FROM checks WHERE check_id=?", (message.text, ))
						temp = cur2.fetchone()
						write_to_admin()
					if temp != None:
						temp=temp[0]
						def clear_final(message):
							if message.text == "Да":
								with lock:
									cursor.execute("SELECT count FROM balance WHERE user_id=?", (message.chat.id,))
									count = cursor.fetchone()
									write_to_admin()
								count = count[0]
								count+=clicks
								with lock:
									cursor.execute("UPDATE balance SET count=? WHERE user_id=?", (count, message.chat.id))
									con.commit()
									write_to_admin()
								with lock:
									cur2.execute("SELECT user_id FROM checks WHERE check_id=?", (temp, ))
									user_id = cur2.fetchone()[0]
									write_to_admin()
								with lock:
									cur2.execute("DELETE FROM checks WHERE check_id=? AND user_id=? AND clicks=?", (temp, user_id, clicks, ))
									con2.commit()
									write_to_admin()
								bot.send_message(message.chat.id, "Ты успешно обналичил чек на сумму "+str(clicks)+" кликов. Твоих кликов: "+str(count))
								bot.send_message(user_id, "Твой чек с кодом "+str(temp)+" и суммой "+str(clicks)+" кликов успешно обналичили!")
								menu.menu(message)
							elif message.text == "Нет":
								menu.menu(message)
						with lock:
							cur2.execute("SELECT clicks FROM checks WHERE check_id=?", (message.text, ))
							clicks=cur2.fetchone()
							write_to_admin()
							clicks=clicks[0]

						clear_final_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
						clear_final_keyboard.add(types.KeyboardButton("Да"), types.KeyboardButton("Нет"))
						send = bot.send_message(message.chat.id, "Ты точно желаешь обналичить чек на "+str(clicks)+" кликов.\nПосле подтверждения отменить операцию невозможно!", reply_markup=clear_final_keyboard)
						bot.register_next_step_handler(send, clear_final)
					else:
						bot.send_message(message.chat.id, "Данного чека не обнаружено! Возвращаю в меню")
			clear_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
			clear_keyboard.add(types.KeyboardButton("Вернуться в меню"))
			send = bot.send_message(call.message.chat.id, "Введите код чека для обналичивания", reply_markup=clear_keyboard)
			bot.register_next_step_handler(send, clear_true)
		elif call.data == "to_menu":
			menu.menu(call.message)

def register_handlers(bot: telebot.TeleBot): 
	bot.register_message_handler(bank, commands=['bank'])
	bot.register_callback_query_handler(bank_callback, func=lambda call: True)