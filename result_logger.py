import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("results/trials.db")

def initialize_db():
    DB_PATH.parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT NOT NULL,
            word_limit_a INTEGER NOT NULL,
            word_limit_b INTEGER NOT NULL,
            actual_words_a INTEGER NOT NULL,
            actual_words_b INTEGER NOT NULL,
            statement_a TEXT NOT NULL,
            statement_b TEXT NOT NULL,
            winner TEXT NOT NULL,
            verdict TEXT NOT NULL,
            precedent_used INTEGER,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

def save_trial(
        case_id,
        word_limit_a,
        word_limit_b,
        statement_a,
        statement_b,
        winner,
        verdict,
        precedent_used
):
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
            INSERT INTO trials (
                case_id,
                word_limit_a,
                word_limit_b,
                actual_words_a,
                actual_words_b,
                statement_a,
                statement_b,
                winner,
                verdict,
                precedent_used,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
        case_id,
        word_limit_a,
        word_limit_b,
        len(statement_a.split()),
        len(statement_b.split()),
        statement_a,
        statement_b,
        winner,
        verdict,
        precedent_used,
        datetime.now().isoformat()
    ))

    connection.commit()
    connection.close()

initialize_db()
