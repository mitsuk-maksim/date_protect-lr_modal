import sqlite3

conn = sqlite3.connect("date_protect.db")
cursor = conn.cursor()

# cursor.execute("""CREATE TABLE table_name
#                   (user text, password text)
#                """)


user = None


# cursor.execute("""
#         insert into users(username, is_superuser)
#         values ('admin', 1)
#         """)
#
# cursor.execute("""
#         insert into users(username, is_superuser)
#         values ('adMIn', 1)
#         """)

cursor.execute(f"""
select username from users where username = 'admin'
""")

print(cursor.fetchall())
conn.commit()

