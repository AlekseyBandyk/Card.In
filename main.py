from create_bot import bot, cursor, cursor1, lock
import psutil
import menu, handle, click, trade, start, quests, profile, minigames, config

@bot.message_handler(commands=['help'])
def help(message):
	bot.send_message(message.chat.id, "Привет, друг! Это сообщение поможет тебе в освоении в Card.In! \n\n\nCard.In представляет собой кликер про карты, которые получаются в ходе игры. \n • | Выполняй задания и получай больше кликов! Изучи задания с помощью /quests или Меню — Квесты\n • | Приглашай друзей и получай особые бонусы в виде кликов и карточек с помощью Меню — Профиль — Реферальная система \n • | Прокачивайся и выходи в ЛИДЕРЫ по кликам!\n • | Играй в мини игры и получай карточки!\n • | Карточки бывают разными, и приносят разный доход:\n\n\nКАРТОЧКИ\nРедкости у карт бывают :\n\n\nОбычные\nНеобычные\nРедкие\nЭпические\nЛегендарные\n\n\n Команды и меню бота\n/authors - узнать авторов игры\n/help - вызвать это сообщение\n/menu - вызвать меню\n/profile - вызвать профиль\n/trade - перейти на торговую площадку\n\n\nУ тебя остались вопросы? Свяжись с нами через обратную связь")

@bot.message_handler(commands=['serv_info'])
def serv_info(message):
	ozy_used = psutil.virtual_memory()
	ozy_used = ozy_used[3]
	ozy_used = ozy_used/10000
	ozy_used = round(ozy_used, 0)
	ozy_perc = psutil.virtual_memory()
	ozy_perc = ozy_perc[2]
	swap_used = psutil.swap_memory()
	swap_used = swap_used[1]
	swap_used = swap_used/10000
	swap_used = round(swap_used, 0)
	swap_perc = psutil.swap_memory()
	swap_perc = swap_perc[3]
	cpu = psutil.cpu_percent(interval=1)
	bot.send_message(message.chat.id, "Использование ОЗУ: "+str(int(ozy_used))+"мб("+str(ozy_perc)+"%)\nИспользование файла подкачки: "+str(int(swap_used))+"мб("+str(swap_perc)+"%)\nИспользование ЦП: "+str(int(cpu))+"%")

@bot.message_handler(commands=['authors'])
def authors(message):
	bot.send_message(message.chat.id, "Авторы CardIn:\n\nКодер/Лидер: <strong>Aleksey 14 02</strong>\nДизайнер/Тестировщик: <strong>ростик(<a href='https://t.me/krsvkdsgnr'>@krsvkdsgnr</a>)</strong>\nГенератор идей/Тестировщик: <strong>Павлик Си́нклев(<a href='https://t.me/Snxly'>@Snxly</a>)</strong>", parse_mode="HTML")

@bot.message_handler(commands=['temp'])
def temp(message):
	bot.send_message(message.chat.id, "Тут ничего нет")

@bot.callback_query_handler(func=lambda call: call.data.startswith("reply:"))
def handle_reply_button(call):
	def send_reply(message, user_id):
		# Отправка ответа пользователю
		bot.send_message(user_id, "Пришёл ответ на твою жалобу: "+message.text)
		bot.send_message(config.owner, f"Ответ отправлен: {user_id}")

	try:
		# Извлечение данных из callback_data
		_, user_id, message_id = call.data.split(":")
		# Отправка администратору просьбы ввести ответ
		sent_message = bot.send_message(config.owner, "Введите ваш ответ:")
		# Хранение данных о пользователе и сообщении для последующего ответа
		bot.register_next_step_handler(sent_message, send_reply, user_id)
	except Exception as e:
		bot.send_message(config.owner, f"Произошла ошибка: {e}")


menu.register_handlers(bot)
click.register_handlers(bot)
trade.register_handlers(bot)
start.register_handlers(bot)
quests.register_handlers(bot)
minigames.register_handlers(bot)
profile.register_handlers(bot)
handle.register_handlers(bot)

def polling_bot():
	try:
		bot.polling(none_stop=True)
	except Exception as e:
		i+=1
		bot.send_message(5493548156, "Bot has been stoped with error: "+e+", but he been restarted. Restart №"+str(i))
		polling_bot()

if __name__ == '__main__':
	i=0
	polling_bot()