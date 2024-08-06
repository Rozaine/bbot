import sqlite3
from .service_sqlite_database import createDB

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Users
                (user_id INTEGER PRIMARY KEY,
                user_name TEXT,
                user_telegram_id TEXT NOT NULL,
                start_at TIMESTAMP NOT NULL,
                last_msg_at TIMESTAMP NOT NULL)
            """)

connection.commit()
connection.close()


def getAllUsersCount():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM Users')
    all_users = cursor.fetchall()
    connection.close()
    return all_users[0][0]


def getTodayRegUsersCount():
    connection = sqlite3.connect('my_database.db',
                                 detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM Users WHERE DATE(start_at) = DATE("now")')
    user_count = cursor.fetchall()
    connection.close()
    return user_count[0][0]


def updateLastUserActivitySql(user_telegram_id, last_msg_at):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET last_msg_at = ? WHERE user_telegram_id = ?', (last_msg_at, user_telegram_id))
    user = cursor.fetchall()
    connection.commit()
    connection.close()


def hasRegistered(user_telegram_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT user_id FROM Users WHERE user_telegram_id = ?', (user_telegram_id,))
    user = cursor.fetchall()
    connection.close()
    return user


def addUserSql(user_telegram_id, user_name, start_at, last_msg_at):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO Users (user_telegram_id, user_name, start_at, last_msg_at) VALUES (?, ?, ?, ?)',
                   (user_telegram_id, user_name, start_at, last_msg_at))

    connection.commit()
    connection.close()
