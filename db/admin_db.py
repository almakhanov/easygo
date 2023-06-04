import psycopg2

from models.admin import Admin
from utils.constants import DB_NAME, DB_USERNAME, DB_PASSWORD, HOST


def get_connection():
    return psycopg2.connect(f"dbname={DB_NAME} user={DB_USERNAME} password={DB_PASSWORD} host={HOST}")


class AdminDB:
    def __init__(self):
        self.conn = get_connection()
        self.create_table()

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS admins (
                    id SERIAL PRIMARY KEY,
                    chat_id VARCHAR(255) NOT NULL,
                    name VARCHAR(255) NOT NULL
                );
            """)
            cur.execute(""" CREATE UNIQUE INDEX IF NOT EXISTS admins_chat_id_idx ON admins (chat_id);""")
            self.conn.commit()

    def get_all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM admins")
        rows = cur.fetchall()
        admins = []
        for row in rows:
            admins.append(Admin(row[1], row[2]))
        return admins

    def insert_all(self, admins):
        cur = self.conn.cursor()
        for admin in admins:
            cur.execute(
                "INSERT INTO admins (chat_id, name) VALUES (%s, %s) ON CONFLICT (chat_id) DO NOTHING RETURNING id",
                (admin.chat_id, admin.name))

        self.conn.commit()
        cur.close()
        self.conn.close()
        return admins
