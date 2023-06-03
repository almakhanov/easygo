import psycopg2
from utils.constants import DB_NAME, DB_USERNAME, DB_PASSWORD, HOST
from models.rent import Rent


def get_connection():
    return psycopg2.connect(f"dbname={DB_NAME} user={DB_USERNAME} password={DB_PASSWORD} host={HOST}")


class RentDB:
    def __init__(self):
        self.conn = get_connection()
        self.create_table()

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS rents (
                    id SERIAL PRIMARY KEY,
                    chat_id VARCHAR(255) NOT NULL,
                    client_fullname VARCHAR(255),
                    product_number INTEGER NOT NULL,
                    product_type VARCHAR(255) NOT NULL,
                    start_date VARCHAR(255) NOT NULL,
                    end_date VARCHAR(255) NOT NULL,
                    price INTEGER NOT NULL,
                    payment_type VARCHAR(255) NOT NULL,
                    rent_status VARCHAR(255) NOT NULL
                );
            """)
            self.conn.commit()

    def get_all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM rents")
        rows = cur.fetchall()

        rents = []
        for row in rows:
            rents.append(Rent(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
        return rents

    def get_latest_rent_by_chat_id(self, chat_id):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM rents WHERE chat_id = %s ORDER BY id DESC LIMIT 1;
            """, (chat_id,))
            row = cur.fetchone()
            if row:
                return Rent(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
            else:
                return None

    def get_rents_by_chat_id(self, chat_id):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM rents WHERE chat_id = %s;
            """, (chat_id,))
            results = cur.fetchall()
            rents = []
            for row in results:
                rent = Rent(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
                rents.append(rent)
            return rents

    def insert(self, rent):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO rents (chat_id, client_fullname, product_number, product_type, start_date, end_date, price, payment_type, rent_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (rent.chat_id, rent.client_fullname, rent.product_number, rent.product_type, rent.start_date, rent.end_date, rent.price, rent.payment_type, rent.rent_status))

        self.conn.commit()
        cur.close()
        self.conn.close()
        return rent
