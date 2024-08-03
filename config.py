from PIL import Image, ImageDraw, ImageFont
import random

token = "7366838775:AAGwq_DXSn_DswLnqKj6d_waMs5DF-52yZI"
owner = -1002239660093
admins = [
	5493548156,
	6474500045,
	6351852749]

default_cards = ["Кирпичный завод", "Завод ткани", "Ферма", "Оружейный завод", "Завод телефонов",]
different_cards = ["Скорая помощь", "Газовая служба", "МЧС", "Полиция",]
rare_cards = ["Детский сад", "Школа", "Университет",]
epic_cards = ["Электростанция", "Торговый центр",]
legendary_cards = ["Мэрия",]

dcp = {
	"Кирпичный завод": "cards/default_brick.jpg",
	"Завод ткани": "cards/default_cloth.jpg",
	"Ферма": "cards/default_farm.jpg",
	"Оружейный завод": "cards/default_gun.jpg",
	"Завод телефонов": "cards/default_phone.jpg"
} #default_cards_path
dfcp = {
	"Скорая помощь": "cards/different_ambulance.jpg",
	"Газовая служба": "cards/different_gas.jpg",
	"МЧС": "cards/different_mchs.jpg",
	"Полиция": "cards/different_police.jpg",
} #different_cards_path
rcp = {
	"Детский сад": "cards/rare_kindergarten.jpg",
	"Школа": "cards/rare_school.jpg",
	"Университет": "cards/rare_university.jpg",
} #rare_cards_path
ecp = {
	"Электростанция": "cards/epic_powerstation.jpg",
	"Торговый центр": "cards/epic_tradecenter.jpg",
} #epic_cards_path
lcp = {
	"Мэрия": "cards/legendary_cityhall.jpg",
} #legendary_cards_path

mph = {
	"Кирпичный завод": 100,
	"Завод ткани": 70,
	"Ферма": 50,
	"Оружейный завод": 120,
	"Завод телефонов": 150,
	"Скорая помощь": 330,
	"Газовая служба": 230,
	"МЧС": 265,
	"Полиция": 350,
	"Детский сад": 400,
	"Школа": 450,
	"Университет": 500,
	"Электростанция": 700,
	"Торговый центр": 650,
	"Мэрия": 1000,
}

choices_for_game2 = {
	1: [2, 4, 6, 8, 10],
	2: [1, 3, 5, 7, 9],
	3: [3, 6, 9, 12, 15],
	4: [5, 10, 15, 20, 25],
	5: [2, 5, 8, 11, 14],
	6: [1, 4, 9, 16, 25],
	7: [4, 8, 12, 16, 20],
	8: [7, 14, 21, 28, 35],
	9: [2, 6, 12, 18, 24],
	10: [10, 20, 30, 40, 50],
	11: [2, 5, 10, 17, 26],
	12: [3, 6, 11, 18, 27],
	13: [4, 8, 14, 22, 32],
	14: [2, 7, 14, 23, 34],
	15: [5, 12, 21, 32, 45],
	16: [1, 6, 15, 28, 45],
	17: [7, 14, 23, 34, 47],
	18: [3, 11, 21, 33, 47],
	19: [6, 13, 22, 33, 46],
	20: [2, 6, 12, 20, 30],
	21: [1, 3, 6, 10, 15],
	22: [5, 11, 19, 29, 41],
	23: [4, 16, 36, 64, 100],
	24: [1, 5, 14, 30, 55],
	25: [2, 7, 14, 23, 34],
	26: [3, 9, 18, 30, 45],
	27: [1, 8, 27, 64, 125],
	28: [5, 20, 45, 80, 125],
}

shifr_words = [
	"лкюч", 
	"яыкз", 
	"лтсо", 
	"слит", 
	"груд", 
	"зжьин", 
	"дмо", 
	"ьпут", 
	"нсо", 
	"стве", 
	"сел", 
	"днье", 
	"нчьо", 
	"игакн", 
	"имр", 
	"адов", 
	"адс", 
	"едл", 
	"укар", 
	"шму", 
	"тко", 
	"окс", 
	"рад", 
	"глу", 
	"чса", 
	"грао",
] #game3
true_words = [
	"ключ",
	"язык",
	"стол",
	"лист",
	"друг",
	"жизнь",
	"дом",
	"путь",
	"сон",
	"свет",
	"лес",
	"день",
	"ночь",
	"книга",
	"мир",
	"вода",
	"сад",
	"лед",
	"рука",
	"шум",
	"кот",
	"сок",
	"дар",
	"луг",
	"час",
	"гора"
] #game3

letters_for_bank = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

def get_card(path, name):
	temp = path[name]
	image = Image.open(temp)
	return image

def get_mph(name):
	a=0
	for i in name:
		try:
			a=a+mph[i]
		except:
			a+=0
	return a

def get_need_card(name):
	if name in default_cards:
		return "default_card"
	elif name in different_cards:
		return "different_card"
	elif name in rare_cards:
		return "rare_card"
	elif name in epic_cards:
		return "epic_card"
	elif name in legendary_cards:
		return "legendary_card"