class User(object):
    __id = None
    username = None
    __hashed_password = None
    email = None

    def __init__(self):
        self.__id = -1
        self.username = ""
        self.email = ""
        self.__hashed_password = ""

    @staticmethod
    def load_user_by_id(cursor, user_id):
        sql = "SELECT id, email, username, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (user_id,))  # (user_id, ) - bo tworzymy krotkę
        data = cursor.fetchone()
        if data:
            loaded_user = User()
            loaded_user.__id = data[0]
            loaded_user.email = data[1]
            loaded_user.username = data[2]
            loaded_user.__hashed_password = data[3]
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, email, username, hashed_password FROM users"
        ret = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_user = User()
            loaded_user.__id = row[0]
            loaded_user.email = row[1]
            loaded_user.username = row[2]
            loaded_user.__hashed_password = row[3]
            ret.append(loaded_user)
        return ret

    @property
    def id(self):
        return self.__id

    @property
    def hashed_password(self):
        return self.__hashed_password

    def set_password(self, password):
    # def set_password(self, password, salt):
        self.__hashed_password = password
        # self.__hashed_password = password_hash(password, salt)

    def save_to_db(self, cursor):
        if self.__id == -1:
            # saving new instance using prepared statements
            sql = """INSERT INTO users(email, username, hashed_password)
                     VALUES(%s, %s, %s) RETURNING id"""
            values = (self.email, self.username, self.hashed_password)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()[0]  # albo cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE users SET email=%s, username=%s, hashed_password=%s WHERE id=%s"""
            values = (self.email, self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    def delete(self, cursor):
        sql = "DELETE FROM users WHERE id=%s"
        cursor.execute(sql, (self.__id, ))
        self.__id = -1
        return True