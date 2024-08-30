import datetime
import bus_config

def lopatina_4():
	grafic = []
	data=""
	full_date = datetime.datetime.now()
	date_id = int(full_date.strftime("%w"))
	if date_id < 6:
		grafic.append(bus_config.lopatina_4_86_r)
		grafic.append(bus_config.lopatina_4_33_r)
	else:
		grafic = bus_config.lopatina_4_86_v
	list_id=0
	for i in grafic:
		if len(grafic) == 1:
			el=0
			for time in i:
				if int(time.split(":")[0]) == full_date.hour():
					while int(time.split(":")[0]) < full_date.minute():
						pass
					near = time
					el+=1
					seq = i[el]
					break
			data = "86: Ближайший в "+near+", следующий в "+seq
		elif len(grafic) == 2:
			el=0
			for time in i:
				if list_id == 0:
					if int(time.split(":")[0]) > full_date.hour or int(time.split(":")[0]) == full_date.hour:
						if int(time.split(":")[1]) >= full_date.minute:
							near = time
							el+=1
							seq = i[el]
							data = "86: Ближайший в "+near+", следующий в "+seq+"\n"
							el=0
							break
				if list_id == 1:
					if int(time.split(":")[0]) > full_date.hour or int(time.split(":")[0]) == full_date.hour:
						if int(time.split(":")[1]) >= full_date.minute:
							near = i[el-1]
							seq = time
							data += "33: Ближайший в "+near+", следующий в "+seq
							break
				el+=1
		list_id+=1

	return data