import sqlite3
con = sqlite3.connect("trade.db", check_same_thread=False)
cursor = con.cursor()

for i in range(1):
	cursor.execute("INSERT INTO trade (user_id, product_name, product_price, product_date) VALUES (?, ?, ?, ?)", (6426582300, "Кирпичный завод", 22, "18.06.2024",))
	con.commit()
print("ALL DONEEEEEEE!!!!!!!!!!")