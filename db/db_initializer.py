from db.banner_db import BannerDB
from db.client_db import ClientDB
from db.product_db import ProductDB
from models.banner import Banner
from models.product import Product
from models.product_type import ProductType
from models.status import Status


def init_db() -> None:
    # Initialize databases
    product_db = ProductDB()
    client_db = ClientDB()
    banner_db = BannerDB()
    fill_products(product_db)
    fill_banners(banner_db)


def fill_products(product_db) -> None:
    list = [
        Product(number=1, vin="3492051", images=["https://photos.app.goo.gl/5CDT5EZTPTJ1pZzE6"], color="None", model="Honda DIO 34", status=Status.IN_RENT,  product_type=ProductType.HONDA_DIO),
        Product(number=2, vin="3013252", images=["https://photos.app.goo.gl/5CDT5EZTPTJ1pZzE6"], color="None", model="Honda DIO 34", status=Status.ACTIVE, product_type=ProductType.HONDA_DIO),
        Product(number=3, vin="3502974", images=["https://photos.app.goo.gl/5CDT5EZTPTJ1pZzE6"], color="None", model="Honda DIO 34", status=Status.ACTIVE, product_type=ProductType.HONDA_DIO),
        Product(number=4, vin="1520832", images=["https://photos.app.goo.gl/5CDT5EZTPTJ1pZzE6"], color="None", model="Honda DIO 34", status=Status.ACTIVE, product_type=ProductType.HONDA_DIO),
        Product(number=5, vin="3456826", images=["https://photos.app.goo.gl/5CDT5EZTPTJ1pZzE6"], color="None", model="Honda DIO 34", status=Status.ACTIVE, product_type=ProductType.HONDA_DIO),
        Product(number=6, vin="3101495", images=["https://photos.app.goo.gl/5CDT5EZTPTJ1pZzE6"], color="None", model="Honda DIO 34", status=Status.ACTIVE, product_type=ProductType.HONDA_DIO),
        Product(number=7, vin="3408937", images=["https://photos.app.goo.gl/5CDT5EZTPTJ1pZzE6"], color="None", model="Honda DIO 34", status=Status.ACTIVE, product_type=ProductType.HONDA_DIO),
        Product(number=8, vin="1537399", images=["https://photos.app.goo.gl/5CDT5EZTPTJ1pZzE6"], color="None", model="Honda DIO 34", status=Status.ACTIVE, product_type=ProductType.HONDA_DIO),
        Product(number=9, vin="1208346", images=["https://photos.app.goo.gl/5CDT5EZTPTJ1pZzE6"], color="None", model="Honda DIO 34", status=Status.ACTIVE, product_type=ProductType.HONDA_DIO),
        Product(number=10, vin="1305557", images=["https://photos.app.goo.gl/5CDT5EZTPTJ1pZzE6"], color="None", model="Honda DIO 34", status=Status.ACTIVE, product_type=ProductType.HONDA_DIO),
        Product(number=11, vin="1556655", images=["https://photos.app.goo.gl/5CDT5EZTPTJ1pZzE6"], color="None", model="Honda DIO 35", status=Status.ACTIVE, product_type=ProductType.HONDA_DIO),
        Product(number=12, vin="1569829", images=["https://photos.app.goo.gl/5CDT5EZTPTJ1pZzE6"], color="None", model="Honda DIO 35", status=Status.ACTIVE, product_type=ProductType.HONDA_DIO),
        Product(number=13, vin="3448477", images=["https://photos.app.goo.gl/5CDT5EZTPTJ1pZzE6"], color="None", model="Honda DIO 34", status=Status.ACTIVE, product_type=ProductType.HONDA_DIO),
        Product(number=14, vin="3115917", images=["https://photos.app.goo.gl/5CDT5EZTPTJ1pZzE6"], color="None", model="Honda DIO 34", status=Status.ACTIVE, product_type=ProductType.HONDA_DIO),
        Product(number=15, vin="1539234", images=["https://photos.app.goo.gl/5CDT5EZTPTJ1pZzE6"], color="None", model="Honda DIO 35", status=Status.ACTIVE, product_type=ProductType.HONDA_DIO),
        Product(number=16, vin="1758946", images=["https://photos.app.goo.gl/5CDT5EZTPTJ1pZzE6"], color="None", model="Honda DIO 35", status=Status.INACTIVE, product_type=ProductType.HONDA_DIO),
        Product(number=17, vin="1111111", images=["https://photos.app.goo.gl/LGSQTy3DWCH46qwc7"], color="Белый", model="Vilimi M8", status=Status.ACTIVE, product_type=ProductType.VILIMI_M8)
    ]
    product_db.insert_all(list)


def fill_banners(banner_db) -> None:
    list = [
        Banner(pricePerWeek=25000, pricePerDay=7000, model="Honda DIO 34", image="https://photos.app.goo.gl/UWMv5x6YM5KkJoWD6", product_type=ProductType.HONDA_DIO),
        Banner(pricePerWeek=30000, pricePerDay=9000, model="Vilimi M8", image="https://photos.app.goo.gl/KJWpxfEHJipgbagu5", product_type=ProductType.VILIMI_M8)
    ]
    banner_db.insert_all(list)
