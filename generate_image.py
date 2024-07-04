from PIL import Image, ImageDraw, ImageFont

def gen_profile(name, clicks, friends):
	image = Image.open("templates/profile.jpg")
	font = ImageFont.truetype("shrift.ttf", 60)
	drawer = ImageDraw.Draw(image)
	drawer.text((200, 245), name, font=font, fill='white') 
	drawer.text((660, 335), clicks, font=font, fill='white')
	drawer.text((750, 410), friends, font=font, fill='white')
	return image

def gen_game3(word):
	image = Image.open("templates/game3.jpg")
	font = ImageFont.truetype("shrift.ttf", 60)
	drawer = ImageDraw.Draw(image)
	text_width = font.getmask(word).getbbox()[2]
	text_height = font.getmask(word).getbbox()[3]
	text_x = 700  # Изменили координату X для текста
	text_y = 630  # Изменили координату Y для текста
	rect_x = text_x
	rect_y = text_y + text_height - 13  # Добавляем смещение для прямоугольника
	rect_width = text_width
	rect_height = 50  # Высота прямоугольника, можно настроить под свои нужды
	rect_bbox = (rect_x, rect_y, rect_x + rect_width, rect_y + rect_height)
	drawer.rectangle(rect_bbox, fill="red")
	drawer.text((text_x, text_y), word, font=font, fill="white")  # Рисуем текст
	return image