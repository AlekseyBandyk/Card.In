import telebot
from telebot import types
import generate_image as gen
import threading
from create_bot import bot, cursor, cursor1, lock

@bot.message_handler(commands=['profile'])
def profile(message):
	with lock:
		cursor.execute("SELECT user_id FROM balance WHERE user_id=?", (message.chat.id,))
		temp = cursor.fetchone()
	if temp == None:
		with lock:
			cursor.execute("INSERT INTO balance (user_id, count, default_card, different_card, rare_card, epic_card, legendary_card, wins, quest1, quest2, quest3, start_time, mph) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (message.chat.id, 1, "", "", "", "", "", 0, False, False, False, 0, 0))
	with lock:
		cursor.execute("SELECT count FROM balance WHERE user_id=?", (message.chat.id,))
		count = cursor.fetchone()
	count = count[0]
	with lock:
		cursor.execute("SELECT referrer FROM balance WHERE referrer=?", (message.chat.id,))
		referrers = cursor.fetchall()
	if referrers == None:
		referrers = 0
	else:
		referrers = len(referrers)
	with lock:
		cursor.execute("SELECT default_card FROM balance WHERE user_id=?", (message.chat.id,))
		temp1 = cursor.fetchone()
	temp1 = str(temp1)
	a = len(temp1)-3
	temp1 = temp1[2:a]
	with lock:
		cursor.execute("SELECT different_card FROM balance WHERE user_id=?", (message.chat.id,))
		temp2 = cursor.fetchone()
	temp2 = str(temp2)
	a = len(temp2)-3
	temp2 = temp2[2:a]
	with lock:
		cursor.execute("SELECT rare_card FROM balance WHERE user_id=?", (message.chat.id,))
		temp3 = cursor.fetchone()
	temp3 = str(temp3)
	a = len(temp3)-3
	temp3 = temp3[2:a]
	with lock:
		cursor.execute("SELECT epic_card FROM balance WHERE user_id=?", (message.chat.id,))
		temp4 = cursor.fetchone()
	temp4 = str(temp4)
	a = len(temp4)-3
	temp4 = temp4[2:a]
	with lock:
		cursor.execute("SELECT legendary_card FROM balance WHERE user_id=?", (message.chat.id,))
		temp5 = cursor.fetchone()
	temp5 = str(temp5)
	a = len(temp5)-3
	temp5 = temp5[2:a]
	profile_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
	but_for_men = types.KeyboardButton("Вернуться в меню")
	but_for_ref = types.KeyboardButton("Моя реферальная ссылка")
	but_for_mine = types.KeyboardButton("Доход в час")
	profile_keyboard.add(but_for_men, but_for_ref, but_for_mine)
	bot.send_photo(message.chat.id, gen.gen_profile(message.chat.first_name, str(count), str(referrers)))
	bot.send_message(message.chat.id, "Здравствуйте, "+message.chat.first_name+"\nКликов: "+str(count)+"\n\nОбычные карты: "+temp1+"\nНеобычные карты: "+temp2+"\nРедкие карты: "+temp3+"\nЭпические карты: "+temp4+"\nЛегендарные карты: "+temp5, reply_markup=profile_keyboard)

def register_handlers(bot: telebot.TeleBot):
	bot.register_message_handler(profile, commands=["profile"])