import psycopg2
from utils.constants import DB_NAME, DB_USERNAME, DB_PASSWORD, HOST
from models.client import Client


def get_connection():
    return psycopg2.connect(f"dbname={DB_NAME} user={DB_USERNAME} password={DB_PASSWORD} host={HOST}")


class ClientDB:
    def __init__(self):
        self.conn = get_connection()
        self.create_table()

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id SERIAL PRIMARY KEY,
                    chat_id VARCHAR(255) NOT NULL,
                    username VARCHAR(255),
                    phone VARCHAR(255),
                    iin VARCHAR(255),
                    firstname VARCHAR(255),
                    lastname VARCHAR(255),
                    second_phone VARCHAR(255),
                    doc_images VARCHAR(3000)[],
                    address VARCHAR(255)
                );
            """)
            cur.execute(""" CREATE UNIQUE INDEX IF NOT EXISTS clients_chat_id_idx ON clients (chat_id);""")
            self.conn.commit()

    def get_all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM clients")
        rows = cur.fetchall()

        clients = []
        for row in rows:
            clients.append(Client(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
        return clients

    def get_client(self, chat_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM clients WHERE chat_id = %s", (chat_id,))
        row = cur.fetchone()
        if row is None:
            return None
        else:
            return Client(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])

    def insert_client(self, client):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO clients (chat_id, username, phone, iin, firstname, lastname, second_phone, doc_images, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (chat_id) DO NOTHING RETURNING id",
            (client.chat_id, client.username, client.phone, client.iin, client.firstname, client.lastname,
             client.second_phone, client.doc_images, client.address))
        self.conn.commit()
        cur.close()
        self.conn.close()
        return client

    def update_client(self, client):
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE clients
                SET username = %s, phone = %s, iin = %s, firstname = %s, lastname = %s, second_phone = %s, doc_images = %s, address = %s
                WHERE chat_id = %s
            """, (client.username, client.phone, client.iin, client.firstname, client.lastname, client.second_phone, client.doc_images, client.address, client.chat_id))
            self.conn.commit()
