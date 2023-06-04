import requests
from telegram import Update
from telegram.ext import ContextTypes

from chat.utils import HandlerOption
from db.banner_db import BannerDB
from db.price_db import PriceDB
from db.product_db import ProductDB
from models.period import Period
from models.status import Status
from utils.constants import TOKEN


def show_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    banner_db = BannerDB()
    product_db = ProductDB()
    banners = banner_db.get_all()
    products = product_db.get_all()
    price_db = PriceDB()

    for banner in banners:
        print(banner.product_type)
        left_count = 0
        total_count = 0
        for product in products:
            if banner.product_type == product.product_type:
                total_count = total_count + 1
                if product.status == Status.ACTIVE:
                    left_count = left_count + 1

        prices = price_db.get_by_product_type(banner.product_type)

        for price in prices:
            if price.period == Period.ONE_WEEK:
                banner.price_per_week = price.price

            if price.period == Period.ONE_DAY:
                banner.price_per_day = price.price

        banner.left_count = left_count
        banner.total_count = total_count

    for banner in banners:
        try:
            req_body = f'https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={update.effective_chat.id}&caption={banner}&photo={banner.image}'
            resp = requests.get(req_body)
            print(resp.content)
        except Exception as e:
            print(e)
    return HandlerOption.ACTION
