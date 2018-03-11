from psycopg2 import connect
from models import User

# from flask import Flask
#
# app = Flask(__name__)
#

user = 'postgres'
pwd = 'coderslab'
host = 'localhost'
db = 'messanger'


def connection():
    conn = connect(user=user, password=pwd, host=host, database=db)
    conn.autocommit = True
    return conn


def close_conn(conn, cursor):
    cursor.close()
    conn.close()

conn = connection()
cursor = conn.cursor()

# janusz = User()
# janusz.email = "janusz@gmail.com"
# janusz.username = "janusz"
# janusz.save_to_db(cursor)

load_users = User.load_all_users(cursor)
for user in load_users:
    incoming_email = "jan@gmail.com"
    if user.email == incoming_email:
        print(user.username)
    else:
        new_user = User()
        new_user.email = incoming_email
        new_user.set_password("haslo")
        new_user.save_to_db(cursor)

    # if user.email == incoming_email:
    #     incoming_password = "haslo"
    #     new_password = "haslo1"
    #     if user.hashed_password == incoming_password and len(new_password) >= 8:
    #         user.set_password(new_password)
    #         user.save_to_db(cursor)


# User.load_user_by_id(cursor, 6)


# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
#
# if __name__ == '__main__':
#     app.run()
