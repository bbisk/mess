from clcrypto import password_hash


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
        cursor.execute(sql, (user_id,))
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

    def set_password(self, password, salt):
        self.__hashed_password = password_hash(password, salt)

    def save_to_db(self, cursor):
        if self.__id == -1:
            sql = """INSERT INTO users(email, username, hashed_password)
                     VALUES(%s, %s, %s) RETURNING id"""
            values = (self.email, self.username, self.hashed_password)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()[0]
            return True
        else:
            sql = """UPDATE users SET email=%s, username=%s, hashed_password=%s WHERE id=%s"""
            values = (self.email, self.username, self.hashed_password, self.__id)
            cursor.execute(sql, values)
            return True

    def delete(self, cursor):
        sql = "DELETE FROM users WHERE id=%s"
        cursor.execute(sql, (self.__id, ))
        self.__id = -1
        return True


class Message():
    __id = None
    from_id = None
    to_id = None
    text = None
    creation_date = None

    def __init__(self):
        self.__id = -1
        self.from_id = ""
        self.to_id = ""
        self.text = ""
        self.creation_date = ""

    @staticmethod
    def load_message_by_id(cursor, msg_id):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM Messages WHERE id=%s"
        cursor.execute(sql, (msg_id,))
        data = cursor.fetchone()
        if data:
            loaded_msg = Message()
            loaded_msg.__id = data[0]
            loaded_msg.from_id = data[1]
            loaded_msg.to_id = data[2]
            loaded_msg.text = data[3]
            loaded_msg.creation_date = data[4]
            return loaded_msg
        else:
            return None


    @staticmethod
    def load_all_messages(cursor):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM Messages"
        ret = []
        cursor.execute(sql)
        for data in cursor.fetchall():
            loaded_msg = Message()
            loaded_msg.__id = data[0]
            loaded_msg.from_id = data[1]
            loaded_msg.to_id = data[2]
            loaded_msg.text = data[3]
            loaded_msg.creation_date = data[4]
            ret.append(loaded_msg)
        return ret

    @staticmethod
    def load_all_messages_for_user(cursor, to_id):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM Messages WHERE to_id=%s"
        cursor.execute(sql, (to_id, ))
        ret = []
        for data in cursor.fetchall():
            loaded_msg = Message()
            loaded_msg.__id = data[0]
            loaded_msg.from_id = data[1]
            loaded_msg.to_id = data[2]
            loaded_msg.text = data[3]
            loaded_msg.creation_date = data[4]
            ret.append(loaded_msg)
        return ret

    def save_to_db(self, cursor):
        if self.__id == -1:
            sql = """INSERT INTO messages(from_id, to_id, text, creation_date) VALUES(%s, %s, %s, NOW()) RETURNING id"""
            values = (self.from_id, self.to_id, self.text)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()[0]
            return True
        else:
            sql = """UPDATE messages SET from_id=%s, to_id=%s, text=%s WHERE id=%s"""
            values = (self.from_id, self.to_id, self.text, self.__id)
            cursor.execute(sql, values)
            return True