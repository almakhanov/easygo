import psycopg2

from models.price import Price
from utils.constants import DB_NAME, DB_USERNAME, DB_PASSWORD, HOST


def get_connection():
    return psycopg2.connect(f"dbname={DB_NAME} user={DB_USERNAME} password={DB_PASSWORD} host={HOST}")


class PriceDB:
    def __init__(self):
        self.conn = get_connection()
        self.create_table()

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS prices (
                    id SERIAL PRIMARY KEY,
                    product_type VARCHAR(255) NOT NULL,
                    period VARCHAR(255) NOT NULL,
                    price INTEGER NOT NULL,
                    text VARCHAR(255) NOT NULL,
                    days INTEGER NOT NULL
                );
            """)
            self.conn.commit()

    def get_all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM prices")
        rows = cur.fetchall()

        prices = []
        for row in rows:
            prices.append(Price(row[1], row[2], row[3], row[4], row[5]))
        return prices

    def get_by_product_type(self, product_type):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM prices WHERE product_type = %s;
            """, (product_type,))
            results = cur.fetchall()
            prices = []
            for row in results:
                price = Price(row[1], row[2], row[3], row[4], row[5])
                prices.append(price)
            return prices

    def insert_all(self, prices):
        cur = self.conn.cursor()
        for price in prices:
            cur.execute(
                "INSERT INTO prices (product_type, period, price, text, days) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (price.product_type, price.period, price.price, price.text, price.days))

        self.conn.commit()
        cur.close()
        self.conn.close()
        return prices

    def clear(self):
        cur = self.conn.cursor()
        cur.execute(f"DELETE FROM prices;")
        self.conn.commit()
