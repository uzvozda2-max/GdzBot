import sqlite3

DB_NAME = "bot.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # адміни
    cur.execute("""CREATE TABLE IF NOT EXISTS admins (
        user_id INTEGER PRIMARY KEY
    )""")

    # банліст
    cur.execute("""CREATE TABLE IF NOT EXISTS bans (
        user_id INTEGER PRIMARY KEY
    )""")

    # домашка
    cur.execute("""CREATE TABLE IF NOT EXISTS dz (
        user_id INTEGER PRIMARY KEY,
        text TEXT
    )""")

    conn.commit()
    conn.close()


# --- адміни ---
def add_admin(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO admins VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def delete_admin(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM admins WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def get_admins():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM admins")
    admins = [row[0] for row in cur.fetchall()]
    conn.close()
    return admins


# --- бан ---
def add_ban(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO bans VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def remove_ban(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM bans WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def get_bans():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM bans")
    bans = [row[0] for row in cur.fetchall()]
    conn.close()
    return bans


# --- домашка ---
def set_dz(user_id: int, text: str):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO dz VALUES (?, ?)", (user_id, text))
    conn.commit()
    conn.close()

def get_dz(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT text FROM dz WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def clear_dz(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM dz WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()
