import sqlite3
def user_reg(message_from_user_id):
    con = sqlite3.connect('bd.sql')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS User_langs(
        id INTEGER PRIMARY KEY, 
        lang TEXT
        )
        ''')
    cur.execute(f"SELECT id FROM User_langs")
    ids = cur.fetchall()

    for elem in ids:
        if message_from_user_id in elem:
            break
    else:
        cur.execute('INSERT INTO User_langs (id, lang) VALUES (?, ?)', (message_from_user_id, 'ru-en'))
    con.commit()
    cur.close()
    con.close()

def get_langs(message_from_user_id):
    con = sqlite3.connect('bd.sql')
    cur = con.cursor()
    cur.execute("SELECT lang FROM User_langs WHERE id = ?", (message_from_user_id,))
    langs = list(cur.fetchone())
    con.commit()
    cur.close()
    con.close()
    return langs

def add_lang(message_from_user_id, lang):
    con = sqlite3.connect('bd.sql')
    cur = con.cursor()
    cur.execute("SELECT id FROM User_langs")
    ids = cur.fetchall()
    for elem in ids:
        if message_from_user_id in elem:
            break
    else:
        cur.execute('INSERT INTO User_langs (id) VALUES (?)', (message_from_user_id,))
    cur.execute("SELECT lang FROM User_langs WHERE id = ?", (message_from_user_id,))
    langs_list = list(cur.fetchone())
    if None in langs_list:
        cur.execute('UPDATE User_langs SET lang = ? WHERE id = ?', (lang, message_from_user_id))
    else:
        langs_list.append(lang)
        langs = set(langs_list)
        new_langs = ' '.join(langs)
        cur.execute('UPDATE User_langs SET lang = ? WHERE id = ?', (new_langs, message_from_user_id))
    con.commit()
    cur.close()
    con.close()

def delete(new_langs, message_from_user_id):
    con = sqlite3.connect('bd.sql')
    cur = con.cursor()
    cur.execute('UPDATE User_langs SET lang = ? WHERE id = ?', (new_langs, message_from_user_id))
    con.commit()
    cur.close()
    con.close()