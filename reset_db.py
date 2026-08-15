import sqlite3
from result_logger import initialize_db, DB_PATH

try:
    initialize_db()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM trials")

    connection.commit()
    connection.close()

    print("Trials database reset.")

except sqlite3.Error as e:
    print(f"reset_db: failed to reset trials database: {e}")