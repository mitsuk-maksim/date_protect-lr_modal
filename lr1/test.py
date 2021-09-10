# import sqlite3
#
# conn = sqlite3.connect("date_protect.db")
# cursor = conn.cursor()
#
# # cursor.execute("""CREATE TABLE table_name
# #                   (user text, password text)
# #                """)
#
#
# user = None
# cursor.execute(f"""
# select username, is_confirm from users
# """)
# print(cursor.fetchall())
# conn.commit()

import re
test = 'wdA'
password = 'e.'
if re.match(".*[A-Z].*", password) and re.match(".*[a-z].*", password) and re.match(".*[~!.......].*", password):
    print(True)
