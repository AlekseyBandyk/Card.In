import telebot
from telebot import types
import config
import datetime
import threading
from menu import menu
from create_bot import bot, cursor, cursor1, lock, con, con1, write_to_admin

def shop(message):
	def buy(message):
		bot.send_message(message.chat.id, "Показываю все предложения...")
		with lock:
			cursor1.execute("SELECT user_id FROM trade")
			user_id = cursor1.fetchall()
			write_to_admin()
		user_id = list(set(user_id))
		a=0
		data = ""
		for i in user_id:
			i = list(i)
			i = i[0]
			with lock:
				cursor1.execute("SELECT product_name FROM trade WHERE user_id=?", (int(i),))
				name = cursor1.fetchall()
				write_to_admin()
			with lock:
				cursor1.execute("SELECT product_price FROM trade WHERE user_id=?", (int(i),))
				price = cursor1.fetchall()
				write_to_admin()
			with lock:
				cursor1.execute("SELECT product_date FROM trade WHERE user_id=?", (int(i),))
				date = cursor1.fetchall()
				write_to_admin()
			for b in range(len(name)):
				a+=1
				name = name[b]
				name = name[0]
				price = price[b]
				price = price[0]
				date = date[b]
				date = date[0]
				data = data+"\n"+str(a)+". "+str(name)+" - "+str(price)+"("+str(date)+")"
		try:
			def choice_buy(message):
				if message.text == "Отменить":
					menu(message)
				else:
					try:
						with lock:
							cursor1.execute("SELECT user_id FROM trade")
							a = cursor1.fetchall()
							write_to_admin()
						a = int(len(a))
						temp = int(message.text)
						if temp <= a:
							with lock:
								cursor1.execute("SELECT user_id FROM trade")
								user_id = cursor1.fetchall()
								write_to_admin()
							user_id = list(set(user_id))
							a=0
							for i in user_id:
								i = list(i)
								i = i[0]
								with lock:
									cursor1.execute("SELECT product_name FROM trade WHERE user_id=?", (int(i),))
									name = cursor1.fetchall()
									write_to_admin()
								with lock:
									cursor1.execute("SELECT product_price FROM trade WHERE user_id=?", (int(i),))
									price = cursor1.fetchall()
									write_to_admin()
								with lock:
									cursor1.execute("SELECT product_date FROM trade WHERE user_id=?", (int(i),))
									date = cursor1.fetchall()
									write_to_admin()
								a+=1
								for b in range(len(name)):
									if a == temp:
										dname = name[b]
										fname = dname[0]
										dprice = price[b]
										fprice = dprice[0]
										ddate = date[b]
										fdate = ddate[0]

							def func_buy_choice(message):
								if message.text == "Да":
									with lock:
										cursor.execute("SELECT ? FROM balance WHERE user_id=?", (config.get_need_card(fname), message.chat.id,))
										tttemp = cursor.fetchone()
										write_to_admin()
									tttemp = str(tttemp)
									if tttemp == "('default_card',)" or tttemp == "None":
										tttemp = fname
									else:
										a = len(tttemp)-3
										tttemp = tttemp[2:a]
										tttemp = tttemp+", "+str(fname)
									with lock:
										cursor.execute("SELECT mph FROM balance WHERE user_id=?", (message.chat.id,))
										temp1 = cursor.fetchone()
										write_to_admin()
									if temp1 == None or temp1 == (None,):
										temp2 = tttemp.split(", ")
										temp1 = config.get_mph(temp2)
									else:
										temp2 = tttemp.split(", ")
										temp1 = temp1[0]
										temp1 = int(temp1)
										temp1+=config.get_mph(temp2)
									with lock:
										cursor.execute("SELECT count FROM balance WHERE user_id=?", (message.chat.id,))
										count = cursor.fetchone()
										write_to_admin()
									count = count[0]
									count = count-fprice
									if count < 0:
										bot.send_message(message.chat.id, "Ошибка! У тебя недостаточно средств для покупки этой карточки!")
										menu(message)
									else:
										with lock:
											cursor1.execute("SELECT user_id FROM trade WHERE product_date = ? AND product_price = ? AND product_name = ?", (fdate, fprice, fname))
											user_id = cursor1.fetchone()
											write_to_admin()
										user_id = user_id[0]
										temp2 = config.get_need_card(fname)
										with lock:
											cursor1.execute("DELETE FROM trade WHERE product_date = ? AND product_price = ? AND product_name = ?", (fdate, fprice, fname,))
											con1.commit()
											write_to_admin()
										with lock:
											cursor.execute("UPDATE balance SET count=?  WHERE user_id=?", (count, message.chat.id))
											con.commit()
											write_to_admin()
										with lock:
											cursor.execute("UPDATE balance SET mph=?  WHERE user_id=?", (temp1, message.chat.id))
											con.commit()
											write_to_admin()
										if temp2 == "default_card":
											with lock:
												cursor.execute("UPDATE balance SET default_card=?  WHERE user_id=?", (tttemp, message.chat.id))
												con.commit()
												write_to_admin()
										elif temp2 == "different_card":
											with lock:
												cursor.execute("UPDATE balance SET different_card=?  WHERE user_id=?", (tttemp, message.chat.id))
												con.commit()
												write_to_admin()
										elif temp2 == "rare_card":
											with lock:
												cursor.execute("UPDATE balance SET rare_card=?  WHERE user_id=?", (tttemp, message.chat.id))
												con.commit()
												write_to_admin()
										elif temp2 == "epic_card":
											with lock:
												cursor.execute("UPDATE balance SET epic_card=?  WHERE user_id=?", (tttemp, message.chat.id))
												con.commit()
												write_to_admin()
										elif temp2 == "legendary_card":
											with lock:
												cursor.execute("UPDATE balance SET legendary_card=?  WHERE user_id=?", (tttemp, message.chat.id))
												con.commit()
												write_to_admin()
										bot.send_message(message.chat.id, "Покупка совершена")
										with lock:
											cursor.execute("SELECT count FROM balance WHERE user_id=?", (user_id,))
											countt = cursor.fetchone()
											write_to_admin()
										countt = countt[0]
										ttempp = round(fprice/10, 0)
										countt = countt+fprice-ttempp
										with lock:
											cursor.execute("UPDATE balance SET count=? WHERE user_id=?", (countt, user_id))
											con.commit()
											write_to_admin()
										bot.send_message(user_id, "Ты успешно продал "+str(fname)+" за "+str(int(fprice-ttempp))+" кликов(клика). 10% комиссии забрано рынком.")
										with lock:
											cursor.execute("SELECT count FROM balance WHERE user_id=?", (5493548156,))
											ccountt = cursor.fetchone()
											write_to_admin()
										ccountt = ccountt[0]
										ttemppp = round(fprice/10, 0)
										ccountt = ccountt+ttemppp
										with lock:
											cursor.execute("UPDATE balance SET count=? WHERE user_id=?", (ccountt, 5493548156))
											con.commit()
											write_to_admin()
								elif message.text == "Нет":
									bot.send_message(message.chat.id, "Покупка прервана, возвращаю в список товаров")
									buy(message)
								else:
									send = bot.send_message(message.chat.id, "Неверный ответ")
									bot.register_next_step_handler(send, func_buy_choice)
							bot.send_message(message.chat.id, "Ваш выбор: "+str(fname)+" - "+str(fprice)+"("+str(fdate)+")")
							buy_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
							yes_choice = types.KeyboardButton("Да")
							no_choice = types.KeyboardButton("Нет")
							buy_keyboard.add(yes_choice, no_choice)
							send = bot.send_message(message.chat.id, "Это последнее предупреждение! Вы желайте купить данный товар", reply_markup=buy_keyboard)
							bot.register_next_step_handler(send, func_buy_choice)

						else:
							bot.send_message(message.chat.id, "Такого варианта нету")
					except:
						bot.send_message(message.chat.id, "Ты ввёл не число")
						buy(message)
			bot.send_message(message.chat.id, data)
			buy_choice_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
			cancel_choice_buy = types.KeyboardButton("Отменить")
			buy_choice_keyboard.add(cancel_choice_buy)
			send = bot.send_message(message.chat.id, "Введите номер покупки", reply_markup=buy_choice_keyboard)
			bot.register_next_step_handler(send, choice_buy)
		except:
			bot.send_message(message.chat.id, "Подходящих предложений нет")

	def sell(message):
		def money_choice_sell(message):
			def final_sell(message):
				def sold(message):
					date = datetime.date.today()
					if message.text == "Да":
						with lock:
							cursor1.execute("INSERT INTO trade (user_id, product_name, product_price, product_date) VALUES (?, ?, ?, ?)", (message.chat.id, tovar, sell_count, date))
							write_to_admin()
						with lock:
							cursor.execute("SELECT ? FROM balance WHERE user_id=?", (config.get_need_card(tovar), message.chat.id,))
							temp52 = cursor.fetchone()
							write_to_admin()
						temp53 = config.get_need_card(tovar)
						temp52 = str(temp52)
						a = len(temp52)-3
						temp52 = temp52[2:a]
						if temp52 != "":
							temp52 = temp52.replace(tovar+", ", "", 1)
							if temp53 == "default_card":
								with lock:
									cursor.execute("UPDATE balance SET default_card=?  WHERE user_id=?", (temp52, message.chat.id))
									con.commit()
									write_to_admin()
							elif temp53 == "different_card":
								with lock:
									cursor.execute("UPDATE balance SET different_card=?  WHERE user_id=?", (temp52, message.chat.id))
									con.commit()
									write_to_admin()
							elif temp53 == "rare_card":
								with lock:
									cursor.execute("UPDATE balance SET rare_card=?  WHERE user_id=?", (temp52, message.chat.id))
									con.commit()
									write_to_admin()
							elif temp53 == "epic_card":
								with lock:
									cursor.execute("UPDATE balance SET epic_card=?  WHERE user_id=?", (temp52, message.chat.id))
									con.commit()
									write_to_admin()
							elif temp53 == "legendary_card":
								with lock:
									cursor.execute("UPDATE balance SET legendary_card=?  WHERE user_id=?", (temp52, message.chat.id))
									con.commit()
									write_to_admin()
							bot.send_message(message.chat.id, "Ты успешно поставил на продажу данную карту")
						else:
							bot.send_message(message.chat.id, "У тебя нету карт")
							menu(message)
					elif message.text == "Нет":
						bot.send_message(message.chat.id, "Продажа отменена")
						menu(message)
				if message.text == "Отменить":
					menu(message)
				else:
					try:
						sell_count = int(message.text)
						final_sell_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
						yes_choice = types.KeyboardButton("Да")
						no_choice = types.KeyboardButton("Нет")
						final_sell_keyboard.add(yes_choice, no_choice)
						bot.send_message(message.chat.id, "Ты продаёшь: "+tovar+" за "+str(sell_count)+" кликов")
						send = bot.send_message(message.chat.id, "Это последнее предупреждение! После нажатия на кнопку Да карточку нельзя будет вернуть", reply_markup=final_sell_keyboard)
						bot.register_next_step_handler(send, sold)
					except:
						bot.send_message(message.chat.id, "Ты ввёл не число")
						money_choice_sell(message)

			if message.text == "Отменить":
				menu(message)
			else:
				money_choice_sell_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
				money_choice_sell_keyboard.add(types.KeyboardButton("Отменить"))
				tovar = message.text
				send = bot.send_message(message.chat.id, "Напиши стоимость товара", reply_markup=money_choice_sell_keyboard)
				bot.register_next_step_handler(send, final_sell)

		choice_card_sell = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		with lock:
			cursor.execute("SELECT default_card FROM balance WHERE user_id=?", (message.chat.id,))
			temp = cursor.fetchall()
			write_to_admin()
		temp = temp[0]
		temp = temp[0]
		print(str(temp))
		if temp !=0:
			temp = "9"+temp
			temp = temp[1:]
			temp = temp.split(", ")
			for i in temp:
				choice_card_sell.add(types.KeyboardButton(i))
		with lock:
			cursor.execute("SELECT different_card FROM balance WHERE user_id=?", (message.chat.id,))
			temp = cursor.fetchall()
			write_to_admin()
		temp = temp[0]
		temp = temp[0]
		print(str(temp))
		if temp !=0:
			temp = "9"+temp
			temp = temp[1:]
			temp = temp.split(", ")
			for i in temp:
				choice_card_sell.add(types.KeyboardButton(i))
		with lock:
			cursor.execute("SELECT rare_card FROM balance WHERE user_id=?", (message.chat.id,))
			temp = cursor.fetchall()
			write_to_admin()
		temp = temp[0]
		temp = temp[0]
		print(str(temp))
		if temp !=0:
			temp = "9"+temp
			temp = temp[1:]
			temp = temp.split(", ")
			for i in temp:
				choice_card_sell.add(types.KeyboardButton(i))
		with lock:
			cursor.execute("SELECT epic_card FROM balance WHERE user_id=?", (message.chat.id,))
			temp = cursor.fetchall()
			write_to_admin()
		temp = temp[0]
		temp = temp[0]
		print(str(temp))
		if temp !=0:
			temp = "9"+temp
			temp = temp[1:]
			temp = temp.split(", ")
			for i in temp:
				choice_card_sell.add(types.KeyboardButton(i))
		with lock:
			cursor.execute("SELECT legendary_card FROM balance WHERE user_id=?", (message.chat.id,))
			temp = cursor.fetchall()
			write_to_admin()
		temp = temp[0]
		temp = temp[0]
		print(str(temp))
		if temp !=0:
			temp = "9"+temp
			temp = temp[1:]
			temp = temp.split(", ")
			for i in temp:
				choice_card_sell.add(types.KeyboardButton(i))
		choice_card_sell.add(types.KeyboardButton("Отменить"))
		send = bot.send_message(message.chat.id, "Выбери карточку для продажи", reply_markup=choice_card_sell)
		bot.register_next_step_handler(send, money_choice_sell)

	def choice(message):
		if message.text == "Купить":
			buy(message)
		elif message.text == "Продать":
			sell(message)
	choices = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
	choice1 = types.KeyboardButton("Купить")
	choice2 = types.KeyboardButton("Продать")
	choices.add(choice1, choice2)
	bot.send_message(message.chat.id, "Привет! Ты попал на торговую площадку Card.In Trade.\nЗдесь ты можешь продавать и покупать карточки.\nПомни, после покупки/продажи клики/карточки вернуть нельзя!")
	send = bot.send_message(message.chat.id, "Что хочешь сделать?", reply_markup=choices)
	bot.register_next_step_handler(send, choice)

def register_handlers(bot: telebot.TeleBot):
	bot.register_message_handler(shop, commands=["trade"])