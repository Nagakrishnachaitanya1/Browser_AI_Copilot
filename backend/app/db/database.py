import sqlite3


def initialize_db():

    connect = sqlite3.connect("chat_history.db")
    try:
        cursor = connect.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS chat_history(
                        id INTEGER PRIMARY KEY,
                        question TEXT NOT NULL,
                        page_content TEXT NOT NULL,
                        answer TEXT NOT NULL
                        )""")

        connect.commit()
    finally:
        connect.close()


if "__main__" == __name__:
    initialize_db()
