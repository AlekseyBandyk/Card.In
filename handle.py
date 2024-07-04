import telebot
from telebot import types
import time
import threading
from create_bot import bot, cursor, cursor1, lock, clicks_for_all, con

import click
import config
import handle
import menu
import profile
import quests
import start
import trade
import minigames

def handle(message):
	if message.text == 'Click!':
		with lock:
			cursor.execute("SELECT user_id FROM balance WHERE user_id=?", (message.chat.id,))
			temp = cursor.fetchone()
		if temp == None:
			with lock:
				cursor.execute("INSERT INTO balance (user_id, count, default_card, different_card, rare_card, epic_card, legendary_card, wins1, wins2, wins3, wins4, wins5, quest1, quest2, quest3, start_time, mph) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (message.chat.id, 1, 0, 0, 0, 0, 0, 0, False, False, False, 0, 0))
		with lock:
			cursor.execute("SELECT count FROM balance WHERE user_id=?", (message.chat.id,))
			count = cursor.fetchone()
		count = count[0]
		count+=1
		with lock:
			cursor.execute("UPDATE balance SET count=? WHERE user_id=?", (count, message.chat.id))
			con.commit()
		global clicks_for_all
		clicks_for_all+=1
		bot.reply_to(message, '+1 клик \n Твоих кликов: '+str(count)+'\n Общих кликов: '+str(clicks_for_all))

	elif message.text == 'Профиль':
		profile.profile(message)

	elif message.text == 'Кликать':
		click.click(message)

	elif message.text == 'Мини-игры':
		minigames.minigames(message)

	elif message.text == 'Вернуться в меню':
		menu.menu(message)

	elif message.text == "Моя реферальная ссылка":
		with lock:
			cursor.execute("SELECT referrer FROM balance WHERE referrer=?", (message.chat.id,))
			referrers = cursor.fetchone()
		if referrers == None:
			referrers = 0
		else:
			referrers = len(referrers)
		link = '`https://t.me/CardInApp_bot?start='+str(message.chat.id)+'`'
		bot.send_message(message.chat.id, "Ваша реферальная ссылка: "+link+"\nПриглашено друзей: "+str(referrers), parse_mode="MarkdownV2")

	elif message.text == "Квесты":
		quests.quest(message)

	elif message.text == 'Торговая площадка':
		trade.shop(message)

	elif message.text == "Обратная связь":
		def send_ask(message):
			forward_message = bot.forward_message(config.owner, message.chat.id, message.message_id)
			markup = types.InlineKeyboardMarkup()
			reply_button = types.InlineKeyboardButton("Ответить", callback_data=f"reply:{message.chat.id}:{forward_message.message_id}")
			markup.add(reply_button)
			bot.send_message(config.owner, f"Новая жалоба от {message.from_user.first_name}(@{message.from_user.username}):", reply_markup=markup)
			bot.send_message(message.chat.id, "Жалоба отправлена, ожидай ответа")
			menu.menu(message)
		send = bot.send_message(message.chat.id, "Ты попал в меню обратной связи. Напиши сюда свою жалобу и наш технический специалист или разработчик ответит на него при первой возможности.\nЕсли жалоба касается возврата чего-либо, то необходимо иметь доказательства")
		bot.register_next_step_handler(send, send_ask)

	elif message.text == 'Доход в час':
		def mphf(message):
			with lock:
				cursor.execute("SELECT start_time FROM balance WHERE user_id=?", (message.chat.id,))
				start_time = cursor.fetchone()
			start_time = start_time[0]
			if message.text == "Начать заработок":
				if start_time == None or start_time == 0:
					start_time = time.time()
					with lock:
						cursor.execute("UPDATE balance SET start_time=? WHERE user_id=?", (start_time, message.chat.id))
						con.commit()
					bot.send_message(message.chat.id, "Ты начал заработок денег")
				elif start_time != None or start_time != 0:
					bot.send_message(message.chat.id, "Ты уже начал заработок денег, ожидай")
			elif message.text == "Получить средства":
				if start_time == None or start_time == 0:
					bot.send_message(message.chat.id, "Ты ещё не начал заработок денег")
				elif start_time != None or start_time != 0:
					temp = time.time()-start_time
					temp = round(temp, 0)
					temp = temp/60
					temp = temp/60
					with lock:
						cursor.execute("SELECT mph FROM balance WHERE user_id=?", (message.chat.id,))
						mph = cursor.fetchone()
					mph = mph[0]
					if temp < 3 and temp > 0:
						if mph > 0:
							start_time = 0
							temp1 = temp*mph
							temp1 = round(temp1, 0)
							with lock:
								cursor.execute("SELECT count FROM balance WHERE user_id=?", (message.chat.id,))
								count = cursor.fetchone()
							count = count[0]
							count = count+temp1
							with lock:
								cursor.execute("UPDATE balance SET start_time=? WHERE user_id=?", (start_time, message.chat.id))
								con.commit()
							with lock:
								cursor.execute("UPDATE balance SET count=? WHERE user_id=?", (count, message.chat.id))
								con.commit()
							bot.send_message(message.chat.id, "Ты закончил заработок и получил "+str(int(temp1))+" кликов")
						else:
							bot.send_message(message.chat.id, "Ты закончил заработок и получил 0 кликов")
			elif message.text == 'Вернуться в меню':
				menu.menu(message)

		mph_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
		but_in_mine1 = types.KeyboardButton("Начать заработок")
		but_in_mine2 = types.KeyboardButton("Получить средства")
		but_for_men = types.KeyboardButton("Вернуться в меню")
		mph_keyboard.add(but_in_mine1, but_in_mine2, but_for_men)

		with lock:
			cursor.execute("SELECT mph FROM balance WHERE user_id=?", (message.chat.id,))
			mph = cursor.fetchone()
		mph = mph[0]

		send = bot.send_message(message.chat.id, "Твой доход в час: "+str(mph)+"\nЖелаешь начать зарабатывать? Помни, доход идёт только 3 часа", reply_markup=mph_keyboard)
		bot.register_next_step_handler(send, mphf)

def register_handlers(bot: telebot.TeleBot):
	bot.register_message_handler(handle, func=lambda message: True)