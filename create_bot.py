import telebot
import config
from telebot import types
import sqlite3
import time
import random
import generate_image as gen
import datetime
import threading

lock = threading.Lock()
con = sqlite3.connect("balance.db", check_same_thread=False)
cursor = con.cursor()
con1 = sqlite3.connect("trade.db", check_same_thread=False)
cursor1 = con1.cursor()
con2 = sqlite3.connect("checks.db", check_same_thread=False)
cur2 = con2.cursor()
clicks_for_all = 1

bot = telebot.TeleBot(config.token)

def write_to_admin():
	last_seen=""
	executs=0
	f=open("admin.txt", "r")
	file=f.read()
	f.close()
	if file == "" or file == "\n":
		executs=1
		line=str(executs)+"\nмомента запуска бота"
	else:
		file=file.split("\n")
		executs=int(file[0])
		last_seen=file[1]
		executs+=1
		line=str(executs)+"\n"+last_seen
	f=open("admin.txt", "w")
	f.write(line)
	f.close()
