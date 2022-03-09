import sqlite3
from mini_logs import log

class DB:
    def __init__(self):
        try:
            self.conn = sqlite3.connect("database.db")
            self.cursor = self.conn.cursor()
        except Exception as e:
            log(str(e), "__init__")

    def insert_patternDB(self, info):
        try:
            self.cursor.execute(f"""INSERT INTO patterns
                VALUES (?, ?)""", info
                )
            self.conn.commit()
        except Exception as e:
            log(str(e), "insert_patternDB")
    
    def insert_wordDB(self, info):
        try:
            self.cursor.execute(f"""INSERT INTO words
                VALUES (?, ?, ?, ?)""", info
                )
            self.conn.commit()
        except Exception as e:
            log(str(e), "insert_wordDB")
    
    def insert_channelDB(self, info):
        try:
            self.cursor.execute(f"""INSERT INTO black_list
                VALUES (?)""", info
                )
            self.conn.commit()
        except Exception as e:
            log(str(e), "insert_channelDB")
            
    def insert_actual_patternDB(self, info):
        try:
            self.cursor.execute('''DELETE FROM actual_pattern''')
            self.cursor.execute(f"""INSERT INTO actual_pattern
                VALUES (?, ?)""", info
                )
            self.conn.commit()
        except Exception as e:
            log(str(e), "insert_actual_patternDB")
        
    #обновление названия у паттерна
    def update_patternDB(self, info):
        try:
            self.cursor.execute(f""" UPDATE patterns
                    SET name_pattern = ?
                    WHERE id_pattern = ?""", info)
            self.conn.commit()
        except Exception as e:
            log(str(e), "update_patternDB")

    #изменение поискового слова
    def update_wordDB(self, info):
        try:
            self.cursor.execute(f""" UPDATE words
                    SET word = ?
                    WHERE id_word = ?""", info)
            self.conn.commit()
        except Exception as e:
            log(str(e), "update_wordDB")

    def update_channelDB(self, info):
        try:
            self.cursor.execute(f""" UPDATE black_list
                    SET id_channel = ?""", info)
            self.conn.commit()
        except Exception as e:
            log(str(e), "update_actual_patternDB")

    #изменение минус-слов
    def update_minus_wordDB(self, info):
        try:
            self.cursor.execute(f""" UPDATE words
                    SET minus_word = ?
                    WHERE id_word = ?""", info)
            self.conn.commit()
        except Exception as e:
            log(str(e), "update_minus_wordDB")

    #изменение актуального (выбранного) паттерна
    def update_actual_patternDB(self, **info):
        try:
            self.cursor.execute(f""" UPDATE actual_pattern
                    SET {', '.join(x + ' = ?' for x in info.keys())}""", tuple(info.values()))
            self.conn.commit()
        except Exception as e:
            log(str(e), "update_actual_patternDB")

    def select_wordDB(self, info):
        try:
            self.cursor.execute(f"""SELECT word, minus_word from words
                WHERE id_word = ?""", info
                )
            value = self.cursor.fetchone()
            return value
        except Exception as e:
            log(str(e), "select_wordDB")

    def select_several_wordDB(self, info):
        try:
            self.cursor.execute(f"""SELECT id_word, word, minus_word, id_pattern from words
                WHERE id_word BETWEEN ? AND ?""", info
                )
            value = self.cursor.fetchall()
            return value
        except Exception as e:
            log(str(e), "select_several_wordDB")

    def select_patternDB(self, info):
        try:
            self.cursor.execute(f"""SELECT id_pattern, name_pattern from patterns
                WHERE id_pattern = ?""", info
                )
            value = self.cursor.fetchone()
            return value
        except Exception as e:
            log(str(e), "select_patternDB")

    def select_actual_patternDB(self):
        try:
            self.cursor.execute(f"""SELECT id_pattern, name_pattern from actual_pattern"""
                )
            value = self.cursor.fetchone()
            return value
        except Exception as e:
            log(str(e), "select_actual_patternDB")

    def select_channelDB(self):
        try:
            self.cursor.execute(f"""SELECT id_channel from black_list"""
                )
            value = self.cursor.fetchone()[0]
            return value
        except Exception as e:
            log(str(e), "select_channelDB")

    def select_several_patternDB(self, info):
        try:
            self.cursor.execute(f"""SELECT id_pattern, name_pattern from patterns
                WHERE id_pattern BETWEEN ? AND ?""", info
                )
            value = self.cursor.fetchall()
            return value
        except Exception as e:
            log(str(e), "select_several_patternDB")

    def select_several_wordDB2(self, info):
        try:
            self.cursor.execute(f"""SELECT id_word, word, minus_word from words
                WHERE id_pattern = ?""", info
                )
            value = self.cursor.fetchall()
            return value
        except Exception as e:
            log(str(e), "select_several_wordDB2")

    def setupDB(self):
        try:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS actual_pattern
                  (id_pattern integer unique, name_pattern text);""")
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS patterns
                  (id_pattern integer unique, name_pattern text);""")
            self.cursor.execute('SELECT count(*) FROM patterns;')
            count = self.cursor.fetchall()
            if count[0][0] < 5:
                for pattern_id in range(5):
                    DB.insert_patternDB(self, (pattern_id+1, f'Pattern{pattern_id+1}'))
                DB.insert_actual_patternDB(self, (1, 'Pattern1'))
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS words
                  (id_word integer unique, id_pattern integer, word text, minus_word text);""")
            self.cursor.execute('SELECT count(*) FROM words;')
            count = self.cursor.fetchall()
            if count[0][0] < 250:
                for pattern_id in range(5):
                    for word_id in range(50):
                        DB.insert_wordDB(self, (pattern_id*50+(word_id+1), pattern_id+1, ' ', ' '))
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS black_list
                  (id_channel text);""")
            return True
        except Exception as e:
            log(str(e), "setupDB")

# a = 200

# while a != 250:
#     a = a+1
#     DB().insert_wordDB(info=(a, 5, f" ", f" "))
#     print(a)
