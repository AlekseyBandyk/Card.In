import sqlite3

con = sqlite3.connect("balance.db")
cursor = con.cursor()
con1 = sqlite3.connect("trade.db")
cursor1 = con1.cursor()
choice = input("1. Только основу, 2. Только площадку, 3. Обе")
choice = int(choice)

if choice == 1:
	cursor.execute("""CREATE TABLE balance
                (user_id long,
                count long,
                default_card str,
                different_card str,
                rare_card str,
                epic_card str,
                legendary_card str,
                wins int,
                quest1 boolean,
                quest2 boolean,
                quest3 boolean,
                start_time float,
                mph long,
                referrer long)
            """)

elif choice == 2:
	cursor1.execute("""CREATE TABLE trade
                (user_id long,
                product_name str,
                product_price long,
                product_date str)
            """)

elif choice == 3:
	cursor.execute("""CREATE TABLE balance
                (user_id long,
                count long,
                default_card str,
                different_card str,
                rare_card str,
                epic_card str,
                legendary_card str,
                wins int,
                quest1 boolean,
                quest2 boolean,
                quest3 boolean,
                start_time float,
                mph long,
                referrer long)
            """)
	cursor1.execute("""CREATE TABLE trade
                (user_id long,
                product_name str,
                product_price long,
                product_date str)
            """)

print("DONE!!!!!!!!!")
