from datetime import datetime, timedelta

import requests
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from chat.utils import payment_type_map
from chat.utils import HandlerOption
from db.client_db import ClientDB
from db.price_db import PriceDB
from db.product_db import ProductDB
from db.rent_db import RentDB
from models.payment_type import PaymentType
from models.rent import Rent
from models.rent_status import RentStatus
from utils.constants import TOKEN


async def complete_rent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    client = ClientDB().get_client(update.effective_chat.id.__str__())
    query_row = context.user_data["rent_data"].split('-')
    product_number = query_row[1]
    period = query_row[2]
    payment_type = query_row[3]
    product = ProductDB().get_product(product_number)
    prices = PriceDB().get_by_product_type(product.product_type)
    price = None
    for p in prices:
        if p.period == period:
            price = p
    now = datetime.now()
    start_date = now.strftime("%d/%m/%Y, %H:%M:%S")
    then = now + timedelta(days=price.days)
    end_date = then.strftime("%d/%m/%Y, %H:%M:%S")

    end_date_text = then.strftime("%d %b %Y, %H:%M")
    # f"<b>Дата возврата:</b> {end_date_text} 🗓\n" \

    user_price = price.price
    price_add_info = ""
    if payment_type == PaymentType.KASPI_RED:
        user_price = price.price / (1 - 0.125)
        price_add_info = " (с 12.5% Red)"

    title = f"<b>Заказ принят</b> ✅\n"\
            f"<b>Мопед:</b> #️⃣ {product.number} - {product.model}\n" \
            f"<b>Период:</b> {price.text}\n" \
            f"<b>Способ оплаты:</b> {payment_type_map[payment_type]}\n" \
            f"<b>Итого:</b> <u>{'{:0,.2f}'.format(user_price)} ₸{price_add_info}</u>"

    rent_db = RentDB()

    rent = Rent(
        chat_id=update.effective_chat.id,
        client_fullname=client.firstname + " " + client.lastname,
        product_number=product_number,
        product_type=product.product_type,
        start_date=start_date,
        end_date=end_date,
        price=price.price,
        payment_type=payment_type,
        rent_status=RentStatus.RESERVE
    )
    rent_db.insert(rent)

    # for admin in ADMINS:
    #     try:
    #         req_body = f'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + admin + '&parse_mode=HTML&text=' + title
    #         resp = requests.get(req_body)
    #         print(resp.content)
    #     except Exception as e:
    #         print(e)

    try:
        await update.callback_query.message.reply_text(title, parse_mode=ParseMode.HTML)
    except:
        await update.message.reply_text(title, parse_mode=ParseMode.HTML)
    return HandlerOption.ACTION
