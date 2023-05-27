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
                    username VARCHAR(255) NOT NULL,
                    phone VARCHAR(255),
                    iin VARCHAR(255),
                    firstname VARCHAR(255),
                    surname VARCHAR(255),
                    second_phone VARCHAR(255),
                    doc_images VARCHAR(255)[],
                    age INTEGER,
                    address VARCHAR(255)
                );
            """)
            self.conn.commit()


def get_all():
    conn = get_connection()

    cur = conn.cursor()
    cur.execute("SELECT * FROM clients")
    rows = cur.fetchall()

    clients = []
    for row in rows:
        clients.append(Client(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
    return clients


def get_client(chat_id):
    # Connect to database
    conn = get_connection()

    # Execute query
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients WHERE chat_id = %s", (chat_id,))
    row = cur.fetchone()

    # Create and return Client object
    return Client(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])


def insert_client(client):
    # Connect to database
    conn = get_connection()

    # Execute query
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO clients (chat_id, username, phone, iin, firstname, surname, second_phone, doc_images, age, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
        (client.chat_id, client.username, client.phone, client.iin, client.firstname, client.surname,
         client.second_phone, client.doc_images, client.age, client.address))
    id = cur.fetchone()[0]

    # Commit changes and close connection
    conn.commit()
    cur.close()
    conn.close()

    # Set client ID and return client object
    client.id = id
    return client
