import sqlite3


def createDB():
    connection = sqlite3.connect('/database/my_database.db')
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS Users
                    (user_id INTEGER PRIMARY KEY,
                    user_name TEXT,
                    user_telegram_id TEXT NOT NULL,
                    start_at TIMESTAMP NOT NULL,
                    last_msg_at TIMESTAMP NOT NULL)
                """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS BooksDownloads
                    (download_id INTEGER PRIMARY KEY,
                    FOREIGN KEY (user_d)  REFERENCES Customers (Id),
                    start_at TIMESTAMP NOT NULL)
                """)

    connection.commit()
    connection.close()
