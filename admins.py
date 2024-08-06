from create_bot import bot, cursor, lock, con, write_to_admin

def add_clicks(user_id, clicks, reason, message):
	with lock:
		cursor.execute("SELECT count FROM balance WHERE user_id=?", (user_id,))
		count = cursor.fetchone()
		write_to_admin()
	count = count[0]
	count+=clicks
	with lock:
		cursor.execute("UPDATE balance SET count=? WHERE user_id=?", (count, user_id,))
		con.commit()
		write_to_admin()
	bot.send_message(message.chat.id, "Перевод был выполнен успешно!")
	bot.send_message(user_id, "Тебе было добавлено "+str(clicks)+" кликов! Причина: "+reason+".\nТвой баланс: "+str(count)+" кликов")

def remove_clicks(user_id, clicks, reason, message):
	with lock:
		cursor.execute("SELECT count FROM balance WHERE user_id=?", (user_id,))
		count = cursor.fetchone()
		write_to_admin()
	count = count[0]
	count-=clicks
	if count < 0:
		bot.send_message(message.chat.id, "Ошибка! У человека недостаточно кликов для удаления!")
	else:
		with lock:
			cursor.execute("UPDATE balance SET count=? WHERE user_id=?", (count, user_id,))
			con.commit()
			write_to_admin()
		bot.send_message(message.chat.id, "Перевод был выполнен успешно!")
		bot.send_message(user_id, "У тебя было удалено "+str(clicks)+" кликов! Причина: "+reason+".\nТвой баланс: "+str(count)+" кликов")


def set_clicks(user_id, clicks, reason, message):
	with lock:
		cursor.execute("SELECT count FROM balance WHERE user_id=?", (user_id,))
		count = cursor.fetchone()
		write_to_admin()
	count = count[0]
	count=clicks
	with lock:
		cursor.execute("UPDATE balance SET count=? WHERE user_id=?", (count, user_id,))
		con.commit()
		write_to_admin()
	bot.send_message(message.chat.id, "Перевод был выполнен успешно!")
	bot.send_message(user_id, "Тебе было задано "+str(clicks)+" кликов! Причина: "+reason+".\nТвой баланс: "+str(count)+" кликов")

def user_info(user_id, message):
	with lock:
		cursor.execute("SELECT user_id FROM balance WHERE user_id=?", (user_id,))
		temp = cursor.fetchone()
		write_to_admin()
	if temp == None:
		bot.send_message(message.chat.id, "Пользователь не найден")
	else:
		data=""
		with lock:
			cursor.execute("SELECT count FROM balance WHERE user_id=?", (user_id,))
			count=cursor.fetchone()[0]
			write_to_admin()
		with lock:
			cursor.execute("SELECT default_card FROM balance WHERE user_id=?", (user_id,))
			default_cards=cursor.fetchone()
			write_to_admin()
		with lock:
			cursor.execute("SELECT different_card FROM balance WHERE user_id=?", (user_id,))
			different_cards=cursor.fetchone()
			write_to_admin()
		with lock:
			cursor.execute("SELECT rare_card FROM balance WHERE user_id=?", (user_id,))
			rare_cards=cursor.fetchone()
			write_to_admin()
		with lock:
			cursor.execute("SELECT epic_card FROM balance WHERE user_id=?", (user_id,))
			epic_cards=cursor.fetchone()
			write_to_admin()
		with lock:
			cursor.execute("SELECT legendary_card FROM balance WHERE user_id=?", (user_id,))
			legendary_cards=cursor.fetchone()
			write_to_admin()
		with lock:
			cursor.execute("SELECT wins1 FROM balance WHERE user_id=?", (user_id,))
			wins1=cursor.fetchone()[0]
			write_to_admin()
		with lock:
			cursor.execute("SELECT wins2 FROM balance WHERE user_id=?", (user_id,))
			wins2=cursor.fetchone()[0]
			write_to_admin()
		with lock:
			cursor.execute("SELECT wins3 FROM balance WHERE user_id=?", (user_id,))
			wins3=cursor.fetchone()[0]
			write_to_admin()
		with lock:
			cursor.execute("SELECT quest1 FROM balance WHERE user_id=?", (user_id,))
			quest1=cursor.fetchone()
			write_to_admin()
		with lock:
			cursor.execute("SELECT quest2 FROM balance WHERE user_id=?", (user_id,))
			quest2=cursor.fetchone()
			write_to_admin()
		with lock:
			cursor.execute("SELECT quest3 FROM balance WHERE user_id=?", (user_id,))
			quest3=cursor.fetchone()
			write_to_admin()
		with lock:
			cursor.execute("SELECT referrer FROM balance WHERE user_id=?", (user_id,))
			referrer=cursor.fetchone()[0]
			write_to_admin()

		data="Пользователь "+bot.get_chat_member(user_id, user_id).user.username+" ("+bot.get_chat_member(user_id, user_id).user.first_name+")\n\nБаланс: "+str(count)+" кликов\nОбычные карты: "+str(default_cards)+"\nНеобычные карты: "+str(different_cards)+"\nРедкие карты: "+str(rare_cards)+"\nЭпические карты: "+str(epic_cards)+"\nЛегендарные карты: "+str(legendary_cards)+"\n\nПобеды в Угадай число: "+str(wins1)+"\nПобеды в Продолжить последовательность: "+str(wins2)+"\nПобеды в Взлом: "+str(wins3)+"\n\n\nID-пригласившего: "+str(referrer)
		bot.send_message(message.chat.id, data)