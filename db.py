import sqlite3

conn = sqlite3.connect('all.db', check_same_thread=False)

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
    user_id INT PRIMARY KEY,
    categories TEXT,
    reply TEXT,
    username TEXT,
    form TEXT);
    """)

conn.commit()


cur.execute("SELECT * FROM users")
res = cur.fetchall()
conn.commit()
print(res)
