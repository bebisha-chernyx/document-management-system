import sqlite3

DATABASE = "documents.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            document_id TEXT PRIMARY KEY,
            filename TEXT NOT NULL UNIQUE,
            file_size INTEGER NOT NULL,
            file_hash TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()