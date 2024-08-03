import telebot
from telebot import types
import time
import threading
from create_bot import bot, cursor, lock, write_to_admin
import menu

def start(message):
	with lock:
		cursor.execute("SELECT user_id FROM balance WHERE user_id=?", (message.chat.id,))
		tempp = cursor.fetchone()
		write_to_admin()

	# обработка реф ссылок
	if " " in message.text:
		referrer_candidate = message.text.split()[1]
		try:
			referrer_candidate = int(referrer_candidate)
			with lock:
				cursor.execute("SELECT user_id FROM balance WHERE user_id=?", (message.chat.id,))
				temp = cursor.fetchone()
				write_to_admin()
			if temp == None:
				with lock:
					cursor.execute("INSERT INTO balance (user_id, count, default_card, different_card, rare_card, epic_card, legendary_card, wins, quest1, quest2, quest3, start_time, mph, referrer) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (message.chat.id, 1, "", "", "", "", "", 0, False, False, False, 0, 0, referrer_candidate))
					write_to_admin()
				bot.send_message(message.chat.id, 'Привет, ты попал на Card.In.\nПохоже, ты пришёл от '+bot.get_chat_member(referrer_candidate, referrer_candidate).user.username+'.\nРегистрирую тебя')
		except ValueError:
			pass

	elif tempp:
		bot.send_message(message.chat.id, 'Привет, можешь продолжать играть')

	else:
		bot.send_message(message.chat.id, 'Привет, ты попал на Card.In.\nПохоже, ты никем не приглашён.\nРегистрирую тебя')
		with lock:
			cursor.execute("INSERT INTO balance (user_id, count, default_card, different_card, rare_card, epic_card, legendary_card, wins, quest1, quest2, quest3, start_time, mph) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (message.chat.id, 1, "", "", "", "", "", 0, False, False, False, 0, 0))
			write_to_admin()

	time.sleep(1)
	bot.send_message(message.chat.id, "Привет, друг! Это сообщение поможет тебе в освоении в Card.In! \n\n\nCard.In представляет собой кликер про карты, которые получаются в ходе игры. \n • | Выполняй задания и получай больше кликов! Изучи задания с помощью /quests или Меню — Квесты\n • | Приглашай друзей и получай особые бонусы в виде кликов и карточек с помощью Меню — Профиль — Реферальная система \n • | Прокачивайся и выходи в ЛИДЕРЫ по кликам!\n • | Играй в мини игры и получай карточки!\n • | Карточки бывают разными, и приносят разный доход:\n\n\nКАРТОЧКИ\nРедкости у карт бывают :\n\n\nОбычные\nНеобычные\nРедкие\nЭпические\nЛегендарные\n\n\n Команды и меню бота\n/authors - узнать авторов игры\n/help - вызвать это сообщение\n/menu - вызвать меню\n/profile - вызвать профиль\n/trade - перейти на торговую площадку\n\n\nУ тебя остались вопросы? Свяжись с нами через обратную связь")
	menu.menu(message)

def register_handlers(bot: telebot.TeleBot):
	bot.register_message_handler(start, commands=["start"])