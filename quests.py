import telebot
from telebot import types
import threading
from create_bot import bot, cursor, lock

@bot.message_handler(commands=['quests'])
def quest(message):
	def check_quests(message):
		if message.text == 'Проверить задания':
			with lock:
				cursor.execute("SELECT count FROM balance WHERE user_id=?", (message.chat.id,))
				temp = cursor.fetchone()
			temp = temp[0]
			with lock:
				cursor.execute("SELECT wins FROM balance WHERE user_id=?", (message.chat.id,))
				temp_wins = cursor.fetchone()
			temp_wins = temp_wins[0]
			with lock:
				cursor.execute("SELECT referrer FROM balance WHERE referrer=?", (message.chat.id,))
				temp_ref = cursor.fetchall()
			temp_ref = len(temp_ref)
			with lock:
				cursor.execute("SELECT quest1 FROM balance WHERE user_id=?", (message.chat.id,))
				temp1 = cursor.fetchone()
			temp1 = temp1[0]
			with lock:
				cursor.execute("SELECT quest2 FROM balance WHERE user_id=?", (message.chat.id,))
				temp2 = cursor.fetchone()
			temp2 = temp2[0]
			with lock:
				cursor.execute("SELECT quest3 FROM balance WHERE user_id=?", (message.chat.id,))
				temp3 = cursor.fetchone()
			temp3 = temp3[0]
			if temp >= 500 and temp1 == 0:
				temp+=500
				with lock:
					cursor.execute("UPDATE balance SET count=? WHERE user_id=?", (temp, message.chat.id))
					con.commit()
				with lock:
					cursor.execute("UPDATE balance SET quest1=? WHERE user_id=?", (1, message.chat.id))
					con.commit()
				bot.send_message(message.chat.id, "Поздравляю ты выполнил задание 2 и получил 500 кликов. Твоих кликов: "+str(temp))
			elif temp_wins >= 3 and temp2 == 0:
				temp+=300
				with lock:
					cursor.execute("UPDATE balance SET count=? WHERE user_id=?", (temp, message.chat.id))
					con.commit()
				with lock:
					cursor.execute("UPDATE balance SET quest2=? WHERE user_id=?", (1, message.chat.id))
					con.commit()
				bot.send_message(message.chat.id, "Поздравляю ты выполнил задание 3 и получил 300 кликов. Твоих кликов: "+str(temp))
			elif temp_ref >= 1 and temp3 == 0:
				temp+=3000
				with lock:
					cursor.execute("UPDATE balance SET count=? WHERE user_id=?", (temp, message.chat.id))
					con.commit()
				with lock:
					cursor.execute("UPDATE balance SET quest3=? WHERE user_id=?", (1, message.chat.id))
					con.commit()
				bot.send_message(message.chat.id, "Поздравляю ты выполнил задание 4 и получил 3000 кликов. Твоих кликов: "+str(temp))
			elif temp1 == 1 and temp2 == 1 and temp3 == 1:
				bot.send_message(message.chat.id, "Ты уже выполнил все задания")
			else:
				bot.send_message(message.chat.id, "Ты не выполнил не одно задание")
		elif message.text == 'Вернуться в меню':
			menu(message)
	quests_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
	but_for_men = types.KeyboardButton("Вернуться в меню")
	but_for_check = types.KeyboardButton("Проверить задания")
	quests_keyboard.add(but_for_men, but_for_check)
	bot.send_message(message.chat.id, "Квесты:")
	send = bot.send_message(message.chat.id, "1. Просмотреть профиль - 100 кликов\n2. Накликать 500 кликов - 500 кликов\n3. Выиграть 3 раза в любой мини-игре - 300 кликов\n4. Пригласить 1 друга - 3000 кликов", reply_markup=quests_keyboard)
	bot.register_next_step_handler(send, check_quests)

def register_handlers(bot: telebot.TeleBot):
	bot.register_message_handler(quest, commands=["quests"])