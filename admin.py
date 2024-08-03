import psutil
import config
import threading
import telebot
import datetime
from telebot import types
import admins
import menu
from create_bot import bot, cursor, lock

def admin(message):
	def choices(message):
		def user_info(message):
			if 2>1:
				admins.user_info(int(message.text), message)
			else:
				send = bot.send_message(message.chat.id, "Вы ввели не id! Введите id пользователя!")
				bot.register_next_step_handler(send, user_info)
		def check_id(message):
			def check_clicks(message):
				def check_reason(message):
					def check_doit(message):
						user_id=datas[0]
						clicks=datas[1]
						reason=datas[2]
						if message.text=="Добавить клики":
							admins.add_clicks(user_id, clicks, reason, message)
						elif message.text=="Удалить клики":
							admins.remove_clicks(user_id, clicks, reason, message)
						elif message.text=="Задать клики":
							admins.set_clicks(user_id, clicks, reason, message)
					datas.append(message.text)
					clicks_admin_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
					add_clicks_choice = types.KeyboardButton("Добавить клики")
					remove_clicks_choice = types.KeyboardButton("Удалить клики")
					set_clicks_choice = types.KeyboardButton("Задать клики")
					clicks_admin_keyboard.add(add_clicks_choice, remove_clicks_choice, set_clicks_choice)
					send = bot.send_message(message.chat.id, "Выберите нужное действие", reply_markup=clicks_admin_keyboard)
					bot.register_next_step_handler(send, check_doit)
				try:
					datas.append(int(message.text))
					send=bot.send_message(message.chat.id, "Введите причину!")
					bot.register_next_step_handler(send, check_reason)
				except:
					send=bot.send_message(message.chat.id, "Вы ввели не число! Введите кол-во кликов!")
					bot.register_next_step_handler(send, check_clicks)
			try:
				datas.append(int(message.text))
				send=bot.send_message(message.chat.id, "Введите кол-во кликов")
				bot.register_next_step_handler(send, check_clicks)
			except:
				send=bot.send_message(message.chat.id, "Введите правильное id пользователя")
				bot.register_next_step_handler(send, check_id)
		if message.text=="Вернуться в меню":
			menu.menu(message)
		elif message.text=="Операции с кликами":
			datas=[]
			send=bot.send_message(message.chat.id, "Введите id пользователя")
			bot.register_next_step_handler(send, check_id)
		elif message.text=="Информация о пользователе":
			send = bot.send_message(message.chat.id, "Введите id пользователя")
			bot.register_next_step_handler(send, user_info)
	f = open("admin.txt", "r")
	file=f.read()
	if file == "":
		executs=0
		date = datetime.datetime.now()
		last_seen=str(date.year)+"."+str(date.month)+"."+str(date.day)+" "+str(date.hour)+":"+str(date.minute)+":"+str(date.second)
	else:
		file=file.split("\n")
		last_seen=file[1]
		executs=file[0]
		executs.replace("\n", "")
		executs=int(executs)
	f.close()
	if message.chat.id in config.admins:
		if message.chat.id == 5493548156:
			bot.send_message(message.chat.id, "Админ-панель без ограничений для вас Алексей!")
		else:
			bot.send_message(message.chat.id, "Здравствуйте "+message.from_user.first_name+"! Загружаю админ-панель!")
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
		bot.send_message(message.chat.id, "Сатанистика использования сервера:\n\n\nИспользование ОЗУ: "+str(int(ozy_used))+"мб("+str(ozy_perc)+"%)\nИспользование файла подкачки: "+str(int(swap_used))+"мб("+str(swap_perc)+"%)\nИспользование ЦП: "+str(int(cpu))+"%"+"\nЗапросов в базу данных с "+last_seen+": "+str(executs))
		with lock:
			cursor.execute("SELECT user_id FROM balance")
			users = cursor.fetchall()
			executs+=1
		len_users = len(users)
		if len_users > 25:
			bot.send_message(message.chat.id, "Всего пользователей в базе данных: "+str(len_users))
		else:
			data = "Всего пользователей в базе данных: "+str(len_users)+"\n\nИмена пользователей:\n"
			for i in users:
				data+=str(i[0])+" : @"+bot.get_chat_member(i, i).user.username+" : "+bot.get_chat_member(i, i).user.first_name+"\n"
			bot.send_message(message.chat.id, data)
		executs=0
		date = datetime.datetime.now()
		last_seen=str(date.year)+"."+str(date.month)+"."+str(date.day)+" "+str(date.hour)+":"+str(date.minute)+":"+str(date.second)
		executs=str(executs)+"\n"
		f = open("admin.txt", "w")
		f.write(executs+last_seen)
		f.close()
		if message.chat.id == 5493548156:
			admin_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
			clicks_choice = types.KeyboardButton("Операции с кликами")
			user_info_choice = types.KeyboardButton("Информация о пользователе")
			to_menu = types.KeyboardButton("Вернуться в меню")
			admin_keyboard.add(clicks_choice, user_info_choice, to_menu)
			send = bot.send_message(message.chat.id, "Выберите дальнейшее действие", reply_markup=admin_keyboard)
			bot.register_next_step_handler(send, choices)
	else:
		bot.send_message(message.chat.id, "У вас недостаточно прав для выполнения данной комманды")

def register_handlers(bot: telebot.TeleBot):
	bot.register_message_handler(admin, commands=["admin"])