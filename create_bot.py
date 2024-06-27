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
clicks_for_all = 1

bot = telebot.TeleBot(config.token)