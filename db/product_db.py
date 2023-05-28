import psycopg2
from utils.constants import DB_NAME, DB_USERNAME, DB_PASSWORD, HOST
from models.product import Product


def get_connection():
    return psycopg2.connect(f"dbname={DB_NAME} user={DB_USERNAME} password={DB_PASSWORD} host={HOST}")


class ProductDB:
    def __init__(self):
        self.conn = get_connection()
        self.create_table()

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY,
                    number INTEGER,
                    vin VARCHAR(255) NOT NULL UNIQUE,
                    images VARCHAR(3000)[],
                    color VARCHAR(255) NOT NULL,
                    model VARCHAR(255) NOT NULL,
                    status VARCHAR(255) NOT NULL,
                    product_type VARCHAR(255) NOT NULL
                );
            """)
            cur.execute(""" CREATE UNIQUE INDEX IF NOT EXISTS products_vin_idx ON products (vin);""")
            self.conn.commit()

    def get_all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM products")
        rows = cur.fetchall()

        # Create and return list of Product objects
        products = []
        for row in rows:
            products.append(Product(row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        return products

    def get_product(self, number):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM products WHERE number = %s", (number,))
        row = cur.fetchone()

        # Create and return Product object
        return Product(row[1], row[2], row[3], row[4], row[5], row[6], row[7])

    def insert_product(self, product):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO products (number, vin, images, color, model, status, product_type) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (vin) DO NOTHING RETURNING id",
            (product.number, product.vin, product.images, product.color, product.model, product.status, product.product_type))
        id = cur.fetchone()[0]

        # Commit changes and close connection
        self.conn.commit()
        cur.close()
        self.conn.close()

        # Set product ID and return product object
        product.id = id
        return product

    def insert_all(self, products):
        cur = self.conn.cursor()
        for product in products:
            cur.execute(
                "INSERT INTO products (number, vin, images, color, model, status, product_type) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (vin) DO NOTHING RETURNING id",
                (product.number, product.vin, product.images, product.color, product.model, product.status, product.product_type))

        self.conn.commit()
        cur.close()
        self.conn.close()
        return products

