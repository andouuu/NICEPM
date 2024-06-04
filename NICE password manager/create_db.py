import sqlite3
import sys

from config import CONFIG

class ExampleDB:
    @staticmethod
    def initialize(database_connection: sqlite3.Connection):
        cursor = database_connection.cursor()
        try:
            print("Dropping existing tables (if present)...")
            cursor.execute("DROP TABLE IF EXISTS users")
            cursor.execute("DROP TABLE IF EXISTS accounts")
        except sqlite3.OperationalError as db_error:
            print(f"Unable to drop table. Error: {db_error}")
        print("Creating tables...")
        cursor.execute(ExampleDB.CREATE_TABLE_users)
        cursor.execute(ExampleDB.CREATE_TABLE_accounts)
       
        database_connection.commit()

    CREATE_TABLE_users = """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        email TEXT NOT NULL,
        session_token TEXT
    )
    """

    CREATE_TABLE_accounts = """
    CREATE TABLE IF NOT EXISTS accounts (
        account_id INTEGER PRIMARY KEY,
        account_name VARCHAR(32) NOT NULL,
        account_password TEXT NOT NULL,
        account_website TEXT,
        account_user_id INTEGER,
        FOREIGN KEY (account_user_id) REFERENCES users(user_id)
    )
    """

def main():
    db_conn = sqlite3.connect(CONFIG["database"]["name"])
    db_conn.row_factory = sqlite3.Row

    ExampleDB.initialize(db_conn)
    db_conn.close()

    print("Database creation finished!")    

    return 0

if __name__ == "__main__":
    sys.exit(main())
