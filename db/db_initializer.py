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
        Product(number=2, vin="3013252", images=["https://photos.app.goo.gl/5CDT5EZTPTJ1pZzE6", "https://photos.app.goo.gl/UWMv5x6YM5KkJoWD6", "https://photos.app.goo.gl/KJWpxfEHJipgbagu5"], color="None", model="Honda DIO 34", status=Status.ACTIVE, product_type=ProductType.HONDA_DIO),
        Product(number=3, vin="3502974", images=["https://lh3.googleusercontent.com/Ewhpk_PprBJyI4INbYS7rLwYbveU2OnEzoBZ-RN6dZZDWB9KiM9hahyXLHoAiCZreqs1iU1Mhnqg6_d33E75h0VbddKDtD47YeA8f26bJC8GMeyIDXwSPSQTfNL5MoRYVBwRmwGVKKEh7ap-4jjDjKYKvK5BCQdpH6Ca8sD30gYHq6HGJxryP4gfpYyT7U7rPDgXCaMFIthhovr-vv9d1Nj_nk2jSC_oT-uDnGbQqPA85b2MIx8btmxjPsw1yo6H2AoZaSmzexBgf5kV-ELxDvYDwOw1gpm_vV-Ae05elSzrIgxUVdtdGa92oA2x83_bk0NqTDWIe-Q06kEEEcC9wmCJiNCPEBU7zsdXBTxw6SmGu2c2RnfgNzHrIMALBzS6itbRM9o9jdZkotcu_qeCv9oLyFjFkNeNYhcwCO5ryQNLxaUqtIUxPNbfFkHsEBk2O9Yj-3iKAT917QH-Gp2gM8Alm7h0JsZefgBcP6KZl80qq8ppPULBg5Scdalv-CK7cAZurQ7MQSjop_1hpZALr3WmaQR2J50GIZVMZAZbK1uuOf66-zsFF1dWpWYeL-z9xAHJjjOgF4QIjMf3UDtmT7Smaq65BRnaXb08wzt_XivTJm0SZ3jEzDlBRbGzSbO08Q-7oClEDRJySR1DKfnxudqXX7H6FH8UcfJx5djb52GCTPVzu1JwlxTt0aVveLISdkd2HFdfkKt5hd6Fiwj0GD0uT1BUq6DRl0pvN_vGNnuBUnhB88hT41KD21OdUxIoL3XsrasA6L54GHAUCs0BcMrXzneG0fxpHr1GGWWN5cPl4Del08lvVOuHdPsesil8d4_MUku-VcUEjanQdgUN23xYoKqQXP5ZkzjpaEwjkIWrRg0BUw0y3hWi59odipSlr5ucdWEQNb315wPRp3ni8yclOzoKq7WRZzlr3pMyr78qYGr-wYIHrpCkw7EKjjojKdMHBd29gmPqD-P1fFJ_RuPYNac_5nKNk9_P26vm_ZxiwFZ03E3O=w640-h480-s-no?authuser=2"], color="None", model="Honda DIO 34", status=Status.ACTIVE, product_type=ProductType.HONDA_DIO),
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
        Product(number=17, vin="1111111", images=["https://lh3.googleusercontent.com/HgN0609y-Bik5UIRcBkHZ-_iAUOXKrkmEU8vxowKVUmFz8otWDrSr5iL_XsGoji1k4GxD5F0WqwhAvI4D6rnvnX1rdDlw0d4ptws602LQAcBSwrP4Z8ngLilZs4g799BbZSDplW70eozo7BWqFTi2KzAZFflY3uEPcJxZW9zRh2d6a4ck9xPRefH7ZjVgZPyUYx_KzYR68mC5EO98YVAmT9eGCqb23DQYKe_-P0a2HQbl5sfzBB2RoF1Lr8KznmBs0sGD-wNpiOp7_o_JwFOtNQL9nB5mJtAD4GSWMPfU4O_qGbFno_IeHno6akuwDm_vechYkJGgGTpKEVLqFf0Agv8tfOjTJAfkO7bbeNV_lWgdKE5hkf9bpeoHn9wOtZZOX0OIEFptsXwjPcUgeJhGrGXoZLYhLh9GIWX02DrAqLNK_CJtRftt0NILyt91ah6RGxyi-sJkO5FBGhTIethLXIFD7p_Qoh_OtfdNlIjeu6cpmv-AeMG0kHv0-T5KogojJyXV7Vqe0o5mEGJfJT_v7MZogi6d6bHorjpZcllfvg1MS2zrwgp1V6CS7fbDjn20hieo40eXx0EDpyN5u_jxpHHMZEi_SRG1NCxZbQZL5N2rFXgBB73s-oTkZlwfpVSoiOgIQA60j_TUJo6d6nRiutVKE-zqcB35vOyr9JmDytGmdCwtpWPizv1_aEa7T6xabOuJuJgYgY_Yjl-p6s-5pHB-3db94Xzfsqzj82weUJHEiJpEeQAWKuntp2SL13qcEmPrsGGl7sTBigbDunpMDchtbs6JutAHWteDydknTgqG36ew3uetrTGrsbojaGvBl518Rbjkfo_leAC5ipVOJV69aDfQmlkz2kV5hySFNv_PEKXkpijGbehAsbm1WeYs8YnH9L-CylsgS0rp2pMuVuQmdZm-c2yZumeWCj1kTKfZz6v_JMUP1IFhuJYu0566zuU9gPwe5fbYuQnqKQr6wCSphg8_IwUP2qvt2b3Hp7JfzPQog4_=w750-h450-s-no?authuser=2"], color="Белый", model="Vilimi M8", status=Status.ACTIVE, product_type=ProductType.VILIMI_M8)
    ]
    product_db.insert_all(list)


def fill_banners(banner_db) -> None:
    list = [
        Banner(pricePerWeek=25000, pricePerDay=7000, model="Honda DIO 34", image="https://lh3.googleusercontent.com/Ewhpk_PprBJyI4INbYS7rLwYbveU2OnEzoBZ-RN6dZZDWB9KiM9hahyXLHoAiCZreqs1iU1Mhnqg6_d33E75h0VbddKDtD47YeA8f26bJC8GMeyIDXwSPSQTfNL5MoRYVBwRmwGVKKEh7ap-4jjDjKYKvK5BCQdpH6Ca8sD30gYHq6HGJxryP4gfpYyT7U7rPDgXCaMFIthhovr-vv9d1Nj_nk2jSC_oT-uDnGbQqPA85b2MIx8btmxjPsw1yo6H2AoZaSmzexBgf5kV-ELxDvYDwOw1gpm_vV-Ae05elSzrIgxUVdtdGa92oA2x83_bk0NqTDWIe-Q06kEEEcC9wmCJiNCPEBU7zsdXBTxw6SmGu2c2RnfgNzHrIMALBzS6itbRM9o9jdZkotcu_qeCv9oLyFjFkNeNYhcwCO5ryQNLxaUqtIUxPNbfFkHsEBk2O9Yj-3iKAT917QH-Gp2gM8Alm7h0JsZefgBcP6KZl80qq8ppPULBg5Scdalv-CK7cAZurQ7MQSjop_1hpZALr3WmaQR2J50GIZVMZAZbK1uuOf66-zsFF1dWpWYeL-z9xAHJjjOgF4QIjMf3UDtmT7Smaq65BRnaXb08wzt_XivTJm0SZ3jEzDlBRbGzSbO08Q-7oClEDRJySR1DKfnxudqXX7H6FH8UcfJx5djb52GCTPVzu1JwlxTt0aVveLISdkd2HFdfkKt5hd6Fiwj0GD0uT1BUq6DRl0pvN_vGNnuBUnhB88hT41KD21OdUxIoL3XsrasA6L54GHAUCs0BcMrXzneG0fxpHr1GGWWN5cPl4Del08lvVOuHdPsesil8d4_MUku-VcUEjanQdgUN23xYoKqQXP5ZkzjpaEwjkIWrRg0BUw0y3hWi59odipSlr5ucdWEQNb315wPRp3ni8yclOzoKq7WRZzlr3pMyr78qYGr-wYIHrpCkw7EKjjojKdMHBd29gmPqD-P1fFJ_RuPYNac_5nKNk9_P26vm_ZxiwFZ03E3O=w640-h480-s-no?authuser=2", product_type=ProductType.HONDA_DIO),
        Banner(pricePerWeek=30000, pricePerDay=9000, model="Vilimi M8", image="https://lh3.googleusercontent.com/HgN0609y-Bik5UIRcBkHZ-_iAUOXKrkmEU8vxowKVUmFz8otWDrSr5iL_XsGoji1k4GxD5F0WqwhAvI4D6rnvnX1rdDlw0d4ptws602LQAcBSwrP4Z8ngLilZs4g799BbZSDplW70eozo7BWqFTi2KzAZFflY3uEPcJxZW9zRh2d6a4ck9xPRefH7ZjVgZPyUYx_KzYR68mC5EO98YVAmT9eGCqb23DQYKe_-P0a2HQbl5sfzBB2RoF1Lr8KznmBs0sGD-wNpiOp7_o_JwFOtNQL9nB5mJtAD4GSWMPfU4O_qGbFno_IeHno6akuwDm_vechYkJGgGTpKEVLqFf0Agv8tfOjTJAfkO7bbeNV_lWgdKE5hkf9bpeoHn9wOtZZOX0OIEFptsXwjPcUgeJhGrGXoZLYhLh9GIWX02DrAqLNK_CJtRftt0NILyt91ah6RGxyi-sJkO5FBGhTIethLXIFD7p_Qoh_OtfdNlIjeu6cpmv-AeMG0kHv0-T5KogojJyXV7Vqe0o5mEGJfJT_v7MZogi6d6bHorjpZcllfvg1MS2zrwgp1V6CS7fbDjn20hieo40eXx0EDpyN5u_jxpHHMZEi_SRG1NCxZbQZL5N2rFXgBB73s-oTkZlwfpVSoiOgIQA60j_TUJo6d6nRiutVKE-zqcB35vOyr9JmDytGmdCwtpWPizv1_aEa7T6xabOuJuJgYgY_Yjl-p6s-5pHB-3db94Xzfsqzj82weUJHEiJpEeQAWKuntp2SL13qcEmPrsGGl7sTBigbDunpMDchtbs6JutAHWteDydknTgqG36ew3uetrTGrsbojaGvBl518Rbjkfo_leAC5ipVOJV69aDfQmlkz2kV5hySFNv_PEKXkpijGbehAsbm1WeYs8YnH9L-CylsgS0rp2pMuVuQmdZm-c2yZumeWCj1kTKfZz6v_JMUP1IFhuJYu0566zuU9gPwe5fbYuQnqKQr6wCSphg8_IwUP2qvt2b3Hp7JfzPQog4_=w750-h450-s-no?authuser=2", product_type=ProductType.VILIMI_M8)
    ]
    banner_db.insert_all(list)
