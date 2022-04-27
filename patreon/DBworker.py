import sqlite3


class DB:
    def __init__(self):
        try:
            self.conn = sqlite3.connect("patreon.db")
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(e)

    def insertDB(self, id_telegram, id_patreon, sum):
        try:
            self.cursor.execute(f"""INSERT INTO users
                    VALUES ({id_telegram}, {id_patreon}, {sum})"""
                                )
            self.conn.commit()
        except Exception as e:
            if str(e) == "UNIQUE constraint failed: users.id_patreon":
                print("Юзверь уже есть в базе")

    def updateDB(self, id_patreon, sum):
        try:
            self.cursor.execute(f""" UPDATE users
                    SET sum = {sum}
                    WHERE id_patreon = {id_patreon}""")
            self.conn.commit()
        except Exception as e:
            print(e)

    def updateDB2(self, id_telegram, info):
        try:
            self.cursor.execute(f""" UPDATE users_bot
                    SET sum = ?, level = ?, expires_in = ?
                    WHERE id_patreon = {id_telegram}""", info)
            self.conn.commit()
        except Exception as e:
            print(e)

    def deleteDB(self, id_telegram):
        try:
            self.cursor.execute(f"""delete from users where id_telegram = {id_telegram}""")
            self.conn.commit()
        except Exception as e:
            print(e)

    def deleteDB2(self, id_telegram):
        try:
            self.cursor.execute(f"""delete from users_bot where id_telegram = {id_telegram}""")
            self.conn.commit()
        except Exception as e:
            print(e)

    def selectDB(self, select, where, request):
        try:
            self.cursor.execute(f""" SELECT {select} FROM users
            WHERE {where} = {request}""")
            value = self.cursor.fetchone()[0]
            return value
        except Exception as e:
            print(e)

    def selectDB_patreons(self):
        try:
            self.cursor.execute("""select id_patreon, id_telegram from users;""")
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def whitelistDB_add(self, id_telegram):
        try:
            self.cursor.execute(f"""INSERT INTO whitelist
                    VALUES ({id_telegram})"""
                                )
            self.conn.commit()
        except Exception as e:
            if str(e) == "UNIQUE constraint failed: whitelist.id_telegram":
                value = True
                return value
            print(e)

    def whitelistDB_remove(self, id_telegram):
        try:
            self.cursor.execute(f"""DELETE FROM whitelist
            WHERE id_telegram = {id_telegram}""")
            self.conn.commit()
        except Exception as e:
            print(e)

    def selectDB_whitelist(self, id_telegram):
        try:
            self.cursor.execute(f""" SELECT id_telegram FROM whitelist
            WHERE id_telegram = {id_telegram}""")
            value = self.cursor.fetchone()[0]
            return value
        except Exception as e:
            if str(e) == "'NoneType' object is not subscriptable":
                value = True
                return value
            print(e)

    def selectDB_patreon_helper(self):
        try:
            self.cursor.execute("""select access_token, refresh_token from patreon_helper order by id desc limit 1;""")
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def insertDB_patreon_helper(self, access_token, refresh_token):
        try:
            self.cursor.execute("""delete from patreon_helper;""")
            self.cursor.execute("""insert into patreon_helper(access_token, refresh_token) values(?, ?)""",
                                (access_token, refresh_token))
            self.conn.commit()
        except Exception as e:
            print(e)

    def selectDB_users_bot(self, info):
        try:
            self.cursor.execute(f""" SELECT * FROM users_bot
            WHERE id_telegram = ?""", info)
            value = self.cursor.fetchall()
            return value
        except Exception as e:
            print(e)

    def selectDB_all_users_bot(self):
        try:
            self.cursor.execute(f""" SELECT * FROM users_bot""")
            value = self.cursor.fetchall()
            return value
        except Exception as e:
            print(e)

    def insertDB_users_bot(self, info):
        try:
            self.cursor.execute(f"""INSERT INTO users_bot
                    VALUES (?, ?, ?, ?)""", info
                                )
            self.conn.commit()
        except Exception as e:
            print(e)

    def deleteDB_users_bot(self, id_telegram):
        try:
            self.cursor.execute(f"""delete from users_bot where id_telegram = {id_telegram}""")
            self.conn.commit()
        except Exception as e:
            print(e)

    def selectDB_wallets(self, info):
        try:
            self.cursor.execute(f""" SELECT * FROM wallets
            WHERE status = ? and type = ?""", info)
            value = self.cursor.fetchall()
            print(value)
            return value
        except Exception as e:
            print(e)

    def selectDB_check_wallets(self, info):
        try:
            self.cursor.execute(f""" SELECT * FROM wallets
            WHERE user_id = ?""", info)
            value = self.cursor.fetchall()
            print(value)
            return value
        except Exception as e:
            print(e)

    def insertDB_wallets(self, info):
        try:
            self.cursor.execute(f"""INSERT INTO wallets
                    VALUES (?, ?, ?, ?)""", info
                                )
            self.conn.commit()
        except Exception as e:
            print(e)

    def updateDB_wallets(self, info):
        try:
            self.cursor.execute(f""" UPDATE wallets
                    SET status = ?, user_id = ?
                    WHERE address = ?""", info)
            self.conn.commit()
        except Exception as e:
            print(e)

    def setupDB(self):
        try:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS users_bot
                  (id_telegram integer unique, sum integer, level text, expires_in integer default 0);""")
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS wallets
                  (type text, address text unique, status integer, user_id integer);""")
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS users
                  (id_telegram integer unique, id_patreon integer unique, sum integer);""")
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS whitelist
                  (id_telegram INTEGER UNIQUE);""")
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS patreon_helper
                  (id integer primary key, access_token text not null, refresh_token text not null);""")
            return True
        except Exception as e:
            print(e)

# DB().insertDB_wallets(info=('BTC', 'YstastA521525ast55', 0, 0))
# DB().insertDB_wallets(info=('BTC', '1EahjiPKXyAFRbTC9HYL67TMQjZZgfFw9g', 0, 0))
# DB().insertDB_wallets(info=('BTC', '1EahjiPKaAAAAAAAAARbTC9HYL67TMQjZZgfFw9g', 0, 0))
# DB().insertDB_users_bot(info=(399010380, 25, "Читатель", "25.05.2022"))
