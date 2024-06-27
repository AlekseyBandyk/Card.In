from PIL import Image, ImageDraw, ImageFont
import random

token = "7366838775:AAHsjtZlYrIpA_V6ML3eg52B4W4SyluCAdY"
owner = -1002239660093

default_cards = ["Кирпичный завод", "Завод ткани", "Ферма", "Оружейный завод", "Завод телефонов",]
different_cards = ["Скорая помощь", "Газовая служба", "МЧС", "Полиция",]
rare_cards = ["Детский сад", "Школа", "Университет",]
epic_cards = ["Электростанция", "Торговый центр",]
legendary_cards = []

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
	"": "cards/epic_powerstation.jpg",
	"": "cards/epic_tradecenter.jpg",
} #epic_cards_path
lcp = {
	
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
}

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