from PIL import Image, ImageDraw, ImageFont
import time

def gen_profile(name, clicks, friends):
	start_time = time.time()  # время начала выполнения
	image = Image.open("templates/profile.jpg")
	font = ImageFont.truetype("shrift.ttf", 60)
	drawer = ImageDraw.Draw(image)
	drawer.text((200, 245), name, font=font, fill='white') 
	drawer.text((660, 335), clicks, font=font, fill='white')
	drawer.text((750, 410), friends, font=font, fill='white')
	end_time = time.time()  # время окончания выполнения
	execution_time = end_time - start_time  # вычисляем время выполнения
	print(f"Время выполнения программы: {execution_time} секунд")
	return image
