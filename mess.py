from psycopg2 import connect
from models import User, Message
import argparse
import re
from clcrypto import generate_salt, check_password

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


def check_user(username):
    load_users = User.load_all_users(cursor)
    for user in load_users:
        if user.email == username or user.username == username:
            return user
    return False


def checked(hashed):
    args = arg_parser()
    pswd_to_check = args.password[0]
    check = check_password(pswd_to_check, hashed)
    if check:
        return True
    else:
        return False


def create_user(username, password):
    if check_user(username) is False:
        new_username = re.search(r'[A-Z0-9a-z._%+-]+@', username)
        if new_username:
            salt = generate_salt()
            new_user = User()
            new_user.username = new_username.group(0)[:-1]
            new_user.email = username
            new_user.set_password(password, salt)
            new_user.save_to_db(cursor)
        else:
            print("Przy zakładaniu konta wprowadź email jako username!")
    else:
        print(username, "już istnieje! Dodaj dodatkowe parametry")


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', nargs=1)
    parser.add_argument('-p', '--password', nargs=1)
    parser.add_argument('-n', '--new-pass', nargs=1)
    parser.add_argument('-e', '--edit', action="store_true")
    parser.add_argument('-l', '--list', action="store_true")
    parser.add_argument('-d', '--delete', action="store_true")
    parser.add_argument('-s', '--send', nargs=1)
    parser.add_argument('-t', '--to', nargs=1)
    return parser.parse_args()


def user_operations():
    args = arg_parser()

    if args.username and args.password and not args.edit and not args.delete and not args.send and not args.list:
        create_user(args.username[0], args.password[0])

    if args.username and args.password and args.edit:
        user = check_user(args.username[0])
        if args.new_pass:
            if checked(user.hashed_password):
                salt = generate_salt()
                user.set_password(args.new_pass[0], salt)
                user.save_to_db(cursor)
            else:
                print("Podaj prawidłowe hasło!")
        else:
            print("Podaj nowe hasło w parametrze -n!")

    if args.username and args.password and args.delete:
        user = check_user(args.username[0])
        if checked(user.hashed_password):
            user.delete(cursor)
        else:
            print("Podaj prawidłowe hasło!")

    if args.list and not args.username and not args.password:
        load_users = User.load_all_users(cursor)
        user_table = "_ID_|__Username__|__Email__\n"
        for user in load_users:
            user_table += " {} | {} | {} \n".format(user.id, user.username, user.email)
        print(user_table)


def msg_operations():
    args = arg_parser()

    if args.username and args.password and args.send:
        user = check_user(args.username[0])
        user_to = check_user(args.to[0])
        if user and user_to:
            if checked(user.hashed_password):
                msg = Message()
                msg.from_id = user.id
                msg.to_id = user_to.id
                msg.text = args.send[0]
                msg.save_to_db(cursor)
            else:
                print("Błędne hasło!")
        else:
            print("Sprawdź dane username i username odbiorcy")

    if args.username and args.password and args.list:
        user = check_user(args.username[0])
        if user and checked(user.hashed_password):
            msg = Message.load_all_messages_for_user(cursor, user.id)
            msg_list = "Otrzymane komunikaty: \n Od | Treść | Utworzono \n"
            for row in msg:
                from_user = User.load_user_by_id(cursor, row.from_id)
                msg_list += " {} | {} | {} \n".format(from_user.username, row.text, row.creation_date)
            print(msg_list)
        else:
            print("Błędny username lub hasło")


if __name__ == '__main__':
    conn = connection()
    cursor = conn.cursor()
    user_operations()
    msg_operations()
    close_conn(conn, cursor)
