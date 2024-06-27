import telebot
from telebot import types
import random
import threading
import config
from create_bot import bot, cursor, lock, con
import menu

def minigames(message):
	def game1(message):
		win_choice = random.randint(1, 3)
		def num_choice(message):
			try:
				numchoice = int(message.text)
				if numchoice == win_choice:
					with lock:
						cursor.execute("SELECT wins FROM balance WHERE user_id=?", (message.chat.id,))
						twins = cursor.fetchone()
					if twins == None or twins == (None,):
						twins = 1
						with lock:
							cursor.execute("INSERT INTO balance (user_id, count, default_card, different_card, rare_card, epic_card, legendary_card, wins, quest1, quest2, quest3, start_time, mph) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (message.chat.id, 1, "", "", "", "", "", 1, False, False, False, 0, 0))
						bot.send_message(message.chat.id, "Ты угадал, твоих побед: "+str(twins))
						game1(message)
					else:
						twins = twins[0]
						twins = int(twins)
						twins+=1
						if twins == 5:
							rand_card = random.choice(config.default_cards)
							bot.send_photo(message.chat.id, config.get_card(config.dcp, rand_card))
							bot.send_message(message.chat.id, "Поздравляю! Ты выиграл карту: "+rand_card)
							with lock:
								cursor.execute("UPDATE balance SET wins=? WHERE user_id=?", (0, message.chat.id))
								con.commit()
							with lock:
								cursor.execute("SELECT default_card FROM balance WHERE user_id=?", (message.chat.id,))
								temp = cursor.fetchone()
							temp = str(temp)
							if temp == "('',)":
								temp = rand_card
							else:
								a = len(temp)-3
								temp = temp[2:a]
								temp = temp+", "+rand_card
							temp2 = temp.split(", ")
							with lock:
								cursor.execute("SELECT mph FROM balance WHERE user_id=?", (message.chat.id,))
								temp1 = cursor.fetchone()
							if temp1 == None or temp1 == (None,):
								temp1 = config.get_mph(temp2)
							else:
								temp1 = temp1[0]
								temp1 = int(temp1)
								temp1+=config.get_mph(temp2)
							with lock:
								cursor.execute("UPDATE balance SET default_card=?, mph=? WHERE user_id=?", (temp, temp1, message.chat.id))
								con.commit
							game1(message)
						else:
							bot.send_message(message.chat.id, "Ты угадал, твоих побед: "+str(twins))
							with lock:
								cursor.execute("UPDATE balance SET wins=? WHERE user_id=?", (twins, message.chat.id))
								con.commit()
							game1(message)
				else:
					bot.send_message(message.chat.id, "Ты не угадал")
					game1(message)
			except:
				if message.text == 'Вернуться в меню':
					menu.menu(message)
				else:
					bot.send_message(message.chat.id, "Ты ввёл не число")
					game1(message)

		game1_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
		but1_for_game1 = types.KeyboardButton('1')
		but2_for_game1 = types.KeyboardButton('2')
		but3_for_game1 = types.KeyboardButton('3')
		but_for_men = types.KeyboardButton("Вернуться в меню")
		game1_keyboard.add(but1_for_game1, but2_for_game1, but3_for_game1, but_for_men)
		send = bot.send_message(message.chat.id, "Выбери число от 1 до 3\nЕсли выиграешь 5 раз - получишь случайную карточку", reply_markup=game1_keyboard)
		bot.register_next_step_handler(send, num_choice)
	msg = message
	games_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
	but_for_game1 = types.KeyboardButton('Угадай число')
	games_keyboard.add(but_for_game1)
	send = bot.send_message(message.chat.id, "Выбери игру", reply_markup=games_keyboard)
	def game_choice(message):
		if message.text == 'Угадай число':
			bot.send_message(message.chat.id, "Игра: Угадай число")
			game1(message)
	bot.register_next_step_handler(send, game_choice)

def register_handlers(bot: telebot.TeleBot):
	bot.register_message_handler(minigames, commands=["minigames"])
