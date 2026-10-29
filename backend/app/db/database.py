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


def save(question: str, page_content: str, answer: str):

    connect = sqlite3.connect("chat_history.db")
    try:
        cursor = connect.cursor()

        cursor.execute(
            """INSERT INTO chat_history (question, page_content, answer)VALUES (?, ?, ?)""",
            (question, page_content, answer),
        )

        last_id = cursor.lastrowid
        connect.commit()

    finally:
        connect.close()

    return last_id


def retrive(id: int):

    connect = sqlite3.connect("chat_history.db")

    try:
        cursor = connect.cursor()
        cursor.execute("""select * from chat_history where id = :id""", {"id": id})

        answer = cursor.fetchone()
    finally:
        connect.close()
    return answer


def retriveAll():

    connect = sqlite3.connect("chat_history.db")

    try:
        cursor = connect.cursor()
        cursor.execute("""select * from chat_history""")

        answer = cursor.fetchall()
    finally:
        connect.close()

    return answer


if "__main__" == __name__:
    initialize_db()
    # save()
    retrive(1)