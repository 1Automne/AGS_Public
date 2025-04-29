import gspread
from datetime import datetime
import re
import logging

gc = gspread.service_account(filename="config/sheetapi.json")

start_date = datetime(2025,1,1)

# Adding data to sheet
def add_day(lesson):
	if lesson.isdigit() or lesson == "-":
		wks = gc.open("AGStatistics").sheet1
		if (datetime.now() - start_date).days + 2 != wks.row_count:
			# формирование даты (чтобы было 2 числа, вместо одного, если число < 10)
			wks.append_row([f"{"0" + str(datetime.now().day) if datetime.now().day < 10 else datetime.now().day}.{"0" + str(datetime.now().month) if datetime.now().month < 10 else datetime.now().month}", lesson])
			update_info_in_file_last7days(wks)
			update_info_in_file_last14days(wks)
			return "Successful"
		else:
			return "Error! Данная строка уже существует."
	else:
		return "Error! Некорректное значение"


# проверка/принудительное добавление информации в бд
def force_add_data():
	wks = gc.open("AGStatistics").sheet1
	if (datetime.now() - start_date).days + 2 != wks.row_count:
		# формирование даты (чтобы было 2 числа, вместо одного, если число < 10)
		wks.append_row([f"{"0" + str(datetime.now().day) if datetime.now().day < 10 else datetime.now().day}.{"0" + str(datetime.now().month) if datetime.now().month < 10 else datetime.now().month}", "-1"])
		update_info_in_file_last7days(wks)
		update_info_in_file_last14days(wks)
		return True
	else:
		return False

# Update data in sheet 
def change_day(date, lesson):
	wks = gc.open("AGStatistics").sheet1
	start_date = datetime(2025,1,1)
	if re.match(r"\d{2}\.\d{2}" , date) is not None:
		day, month  = int(date[0:2]), int(date[3:5])
		if lesson.isdigit() or lesson == "-":
			try:
				selected_date = datetime(2025, month, day)
				row = ((selected_date - start_date).days)+2
				try:
					wks.update_cell(row, 2, lesson)
					if ((datetime.now()-selected_date).days) <= 7:
						update_info_in_file_last7days(wks)
						update_info_in_file_last14days(wks)
					elif 7 < ((datetime.now()-selected_date).days) <= 14:
						update_info_in_file_last14days(wks)
				except gspread.exceptions.APIError:
					return "Введенной даты нет в базе данных, либо она не существует"
			except ValueError:
				return "Error! Неверный формат даты, либо она не существует"
		else:
			return "Error! Некорректное значение"
	else:
		return "Error! Неверный формат даты"
	return f"Successful\n{row} строка изменена\nНовое значение: {lesson}"

# -------

def update_info_on_start():
	wks = gc.open("AGStatistics").sheet1
	update_info_in_file_last7days(wks)
	update_info_in_file_last14days(wks)

# сохранение инфы в файлик 7 дней
def update_info_in_file_last7days(wks):
	result = ''
	f = open("storage/last7days.txt", "w+")
	data = wks.get(f"A{wks.row_count-6}:B{wks.row_count}")   
	for i in data:
		if i[1] == "-":
			f.write(f"{i[0]}: ---\n")
		elif i[1] == "0":
			f.write(f"{i[0]}: Отсутствовал\n")
		elif i[1] == "-1":
			f.write(f"{i[0]}: Нет данных\n")
		else:
			f.write(f"{i[0]}: Пришел к {i[1]}\n")
	f.close()
	logging.info("last7days.txt updated")
	return 0

# сохранение инфы в файлик 14 дней
def update_info_in_file_last14days(wks):
	result = ''
	f = open("storage/last14days.txt", "w+")
	data = wks.get(f"A{wks.row_count-13}:B{wks.row_count}")   
	for i in data:
		if i[1] == "-":
			f.write(f"{i[0]}: ---\n")
		elif i[1] == "0":
			f.write(f"{i[0]}: Отсутствовал\n")
		elif i[1] == "-1":
			f.write(f"{i[0]}: Нет данных\n")			
		else:
			f.write(f"{i[0]}: Пришел к {i[1]}\n")
	f.close()
	logging.info("last14days.txt updated")
	return 0

# -------

# Получение информации (Get Date)
def get_info_by_date(date):
	wks = gc.open("AGStatistics").sheet1
	if re.match(r"\d{2}\.\d{2}" , date) is not None:
		day, month  = int(date[0:2]), int(date[3:5])
		try:
			selected_date = datetime(2025, month, day)
			row = ((selected_date - start_date).days)+2
			try:
				data = wks.cell(row,2).value
				if data == "-":
					return f"{date}: ---"
				elif data == "0":
					return f"{date}: Отсутствовал"
				elif data == "-1":
					return f"{date}: Нет данных"
				else:
					return f"{date}: Пришел к {data}"
			except gspread.exceptions.APIError:
				return "Введенной даты нет в базе данных, либо она не существует"
		except ValueError:
			return "Error! Неверный формат даты"
	else:
		return "Error! Неверный формат даты"

def get_info_from_file_last7days():
	result = "Статистика за 7 дней:\n"
	f = open("storage/last7days.txt")
	for line in f:
		result = result + line
	return result

def get_info_from_file_last14days():
	result = "Статистика за 14 дней:\n"
	f = open("storage/last14days.txt")
	for line in f:
		result = result + line
	return result
# -------------------------------

