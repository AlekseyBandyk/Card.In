import telebot
from telebot import types
import random
import threading
import config
from create_bot import bot, cursor, lock, con, write_to_admin
import menu
import generate_image as gen

def minigames(message):
	def game1(message):
		win_choice = random.randint(1, 3)
		def num_choice(message):
			try:
				numchoice = int(message.text)
				if numchoice == win_choice:
					with lock:
						cursor.execute("SELECT wins1 FROM balance WHERE user_id=?", (message.chat.id,))
						twins1 = cursor.fetchone()
						write_to_admin()
					if twins1 == None or twins1 == (None,):
						twins1 = 1
						with lock:
							cursor.execute("INSERT INTO balance (user_id, count, default_card, different_card, rare_card, epic_card, legendary_card, wins1, wins2, wins3, wins4, wins5, quest1, quest2, quest3, start_time, mph) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (message.chat.id, 1, "", "", "", "", "", 1, 0, 0, 0, 0, False, False, False, 0, 0))
							write_to_admin()
						bot.send_message(message.chat.id, "Ты угадал, твоих побед: "+str(twins1))
						game1(message)
					else:
						twins1 = twins1[0]
						twins1 = int(twins1)
						twins1+=1
						if twins1 == 5:
							rand_card = random.choice(config.default_cards)
							bot.send_photo(message.chat.id, config.get_card(config.dcp, rand_card))
							bot.send_message(message.chat.id, "Поздравляю! Ты выиграл карту: "+rand_card)
							with lock:
								cursor.execute("UPDATE balance SET wins1=? WHERE user_id=?", (0, message.chat.id))
								con.commit()
								write_to_admin()
							with lock:
								cursor.execute("SELECT default_card FROM balance WHERE user_id=?", (message.chat.id,))
								temp = cursor.fetchone()
								write_to_admin()
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
								write_to_admin()
							if temp1 == None or temp1 == (None,):
								temp1 = config.get_mph(temp2)
							else:
								temp1 = temp1[0]
								temp1 = int(temp1)
								temp1+=config.get_mph(temp2)
							with lock:
								cursor.execute("UPDATE balance SET default_card=?, mph=? WHERE user_id=?", (temp, temp1, message.chat.id))
								con.commit()
								write_to_admin()
							game1(message)
						else:
							bot.send_message(message.chat.id, "Ты угадал, твоих побед: "+str(twins1))
							with lock:
								cursor.execute("UPDATE balance SET wins1=? WHERE user_id=?", (twins1, message.chat.id))
								con.commit()
								write_to_admin()
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

	def game2(message):
		x = random.randint(1, 7)
		z=0
		data=""

		progression = config.choices_for_game2[x]
		for i in progression:
			z+=1
			if z == len(progression)-1:
				data+=str(i)
				z=0
				break
			else:
				data+=str(i)+", "

		def game2_choice(message):
			if message.text == "Вернуться в меню":
				menu.menu(message)
			else:
				temp = len(progression)-1
				ttemp=progression[temp]
				try:
					a = int(message.text)
					if a == ttemp:
						with lock:
							cursor.execute("SELECT wins2 FROM balance WHERE user_id=?", (message.chat.id,))
							twins1 = cursor.fetchone()
							write_to_admin()
						if twins1 == None or twins1 == (None,):
							twins1 = 1
							with lock:
								cursor.execute("INSERT INTO balance (user_id, count, default_card, different_card, rare_card, epic_card, legendary_card, wins1, wins2, wins3, wins4, wins5, quest1, quest2, quest3, start_time, mph) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (message.chat.id, 1, "", "", "", "", "", 0, 1, 0, 0, 0, False, False, False, 0, 0))
								write_to_admin()
							bot.send_message(message.chat.id, "Ты угадал, твоих побед: "+str(twins1))
							game2(message)
						else:
							twins1 = twins1[0]
							twins1 = int(twins1)
							twins1+=1
							if twins1 == 8:
								rand_card = random.choice(config.different_cards)
								bot.send_photo(message.chat.id, config.get_card(config.dfcp, rand_card))
								bot.send_message(message.chat.id, "Поздравляю! Ты выиграл карту: "+rand_card)
								with lock:
									cursor.execute("UPDATE balance SET wins2=? WHERE user_id=?", (0, message.chat.id))
									con.commit()
									write_to_admin()
								with lock:
									cursor.execute("SELECT different_card FROM balance WHERE user_id=?", (message.chat.id,))
									temp = cursor.fetchone()
									write_to_admin()
								temp = str(temp)
								if temp == "('',)":
									temp = rand_card
								else:
									x = len(temp)-3
									temp = temp[2:x]
									temp = temp+", "+rand_card
								temp2 = temp.split(", ")
								with lock:
									cursor.execute("SELECT mph FROM balance WHERE user_id=?", (message.chat.id,))
									temp1 = cursor.fetchone()
									write_to_admin()
								if temp1 == None or temp1 == (None,):
									temp1 = config.get_mph(temp2)
								else:
									temp1 = temp1[0]
									temp1 = int(temp1)
									temp1+=config.get_mph(temp2)
								with lock:
									cursor.execute("UPDATE balance SET different_card=?, mph=? WHERE user_id=?", (temp, temp1, message.chat.id))
									con.commit()
									write_to_admin()
								game2(message)
							else:
								bot.send_message(message.chat.id, "Ты угадал, твоих побед: "+str(twins1))
								with lock:
									cursor.execute("UPDATE balance SET wins2=? WHERE user_id=?", (twins1, message.chat.id))
									con.commit()
									write_to_admin()
								game2(message)
					else:
						bot.send_message(message.chat.id, "Ты не угадал")
						game2(message)
				except:
					bot.send_message(message.chat.id, "Ты ввел не число")
					game2(message)
				
		game2_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
		but_for_menu = types.KeyboardButton('Вернуться в меню')
		game2_keyboard.add(but_for_menu)
		send=bot.send_message(message.chat.id, "Продолжи комбинацию чисел: "+data+"\nЕсли выиграешь 8 раз получишь случайную необычную карточку", reply_markup=game2_keyboard)
		bot.register_next_step_handler(send, game2_choice)

	def game3(message):
		x = random.randint(0, 25)
		shifr_word = config.shifr_words[x]
		true_word = config.true_words[x]
		def game3_choice(message):
			if message.text.lower() == true_word:
				with lock:
					cursor.execute("SELECT wins3 FROM balance WHERE user_id=?", (message.chat.id,))
					twins1 = cursor.fetchone()
					write_to_admin()
				if twins1 == None or twins1 == (None,):
					twins1 = 1
					with lock:
						cursor.execute("INSERT INTO balance (user_id, count, default_card, different_card, rare_card, epic_card, legendary_card, wins1, wins2, wins3, wins4, wins5, quest1, quest2, quest3, start_time, mph) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (message.chat.id, 1, "", "", "", "", "", 0, 1, 0, 0, 0, False, False, False, 0, 0))
						write_to_admin()
					bot.send_message(message.chat.id, "Ты угадал, твоих побед: "+str(twins1))
					game3(message)
				else:
					twins1 = twins1[0]
					twins1 = int(twins1)
					twins1+=1
					if twins1 == 12:
						rand_card = random.choice(config.rare_cards)
						bot.send_photo(message.chat.id, config.get_card(config.rcp, rand_card))
						bot.send_message(message.chat.id, "Поздравляю! Ты выиграл карту: "+rand_card)
						with lock:
							cursor.execute("UPDATE balance SET wins3=? WHERE user_id=?", (0, message.chat.id))
							con.commit()
							write_to_admin()
						with lock:
							cursor.execute("SELECT rare_card FROM balance WHERE user_id=?", (message.chat.id,))
							temp = cursor.fetchone()
							write_to_admin()
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
								write_to_admin()
							if temp1 == None or temp1 == (None,):
								temp1 = config.get_mph(temp2)
							else:
								temp1 = temp1[0]
								temp1 = int(temp1)
								temp1+=config.get_mph(temp2)
							with lock:
								cursor.execute("UPDATE balance SET rare_card=?, mph=? WHERE user_id=?", (temp, temp1, message.chat.id))
								con.commit()
								write_to_admin()
						game3(message)
					else:
						bot.send_message(message.chat.id, "Ты угадал, твоих побед: "+str(twins1))
						with lock:
							cursor.execute("UPDATE balance SET wins3=? WHERE user_id=?", (twins1, message.chat.id))
							con.commit()
							write_to_admin()
						game3(message)
			elif message.text ==  "Вернуться в меню":
				menu.menu(message)
			else:
				bot.send_message(message.chat.id, "Ты не угадал")
				game3(message)
		game3_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
		but_for_menu = types.KeyboardButton("Вернуться в меню")
		game3_keyboard.add(but_for_menu)
		bot.send_photo(message.chat.id, gen.gen_game3(shifr_word))
		send = bot.send_message(message.chat.id, "Введи зашифрованное слово. \nЕсли выиграешь 12 раз - получишь случайную карточку", reply_markup=game3_keyboard)
		bot.register_next_step_handler(send, game3_choice)

	games_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
	but_for_game1 = types.KeyboardButton('Угадай число')
	but_for_game2 = types.KeyboardButton('Продолжить последовательность')
	but_for_game3 = types.KeyboardButton('Взлом')
	games_keyboard.add(but_for_game1, but_for_game2, but_for_game3)
	send = bot.send_message(message.chat.id, "Выбери игру", reply_markup=games_keyboard)
	def game_choice(message):
		if message.text == 'Угадай число':
			bot.send_message(message.chat.id, "Игра: Угадай число")
			game1(message)
		elif message.text == 'Продолжить последовательность':
			bot.send_message(message.chat.id, "Игра: Продолжить последовательность")
			game2(message)
		elif message.text == 'Взлом':
			bot.send_message(message.chat.id, "Игра: Взлом")
			game3(message)
	bot.register_next_step_handler(send, game_choice)

def register_handlers(bot: telebot.TeleBot):
	bot.register_message_handler(minigames, commands=["minigames"])
