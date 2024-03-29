import psycopg2

from models.banner import Banner
from utils.constants import DB_NAME, DB_USERNAME, DB_PASSWORD, HOST


def get_connection():
    return psycopg2.connect(f"dbname={DB_NAME} user={DB_USERNAME} password={DB_PASSWORD} host={HOST}")


class BannerDB:
    def __init__(self):
        self.conn = get_connection()
        self.create_table()

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS banners (
                    id SERIAL PRIMARY KEY,
                    model VARCHAR(255) NOT NULL,
                    image VARCHAR(3000) NOT NULL,
                    product_type VARCHAR(255) NOT NULL
                );
            """)
            cur.execute(""" CREATE UNIQUE INDEX IF NOT EXISTS banners_product_type_idx ON banners (product_type);""")
            self.conn.commit()

    def get_all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM banners")
        rows = cur.fetchall()
        banners = []
        for row in rows:
            banners.append(Banner(row[1], row[2], row[3]))
        return banners

    def get_by_product_type(self, product_type):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM banners WHERE product_type = %s", (product_type,))
        row = cur.fetchone()

        return Banner(row[1], row[2], row[3])

    def insert_all(self, banners):
        cur = self.conn.cursor()
        for banner in banners:
            cur.execute(
                "INSERT INTO banners (model, image, product_type) VALUES (%s, %s, %s) ON CONFLICT (product_type) DO NOTHING RETURNING id",
                (banner.model, banner.image, banner.product_type))

        self.conn.commit()
        cur.close()
        self.conn.close()
        return banners
