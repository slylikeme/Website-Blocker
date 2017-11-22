import sqlite3

def connect():
    conn = sqlite3.connect('websites.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS websites (name TEXT)")
    conn.commit()
    conn.close()


def insert(name):
    conn = sqlite3.connect('websites.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO websites VALUES (?)",(name,))
    conn.commit()
    conn.close()


def view():
    conn = sqlite3.connect('websites.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM websites")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_website_list():
    conn = sqlite3.connect('websites.db')
    conn.row_factory = lambda cursor, row: row[0]
    cur = conn.cursor()
    names = cur.execute('SELECT * FROM websites').fetchall()
    conn.close()
    return names


def delete(name):
    conn = sqlite3.connect('websites.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM websites WHERE name=?", (name,))
    conn.commit()
    conn.close()


connect()
