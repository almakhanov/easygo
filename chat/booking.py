from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from chat.utils import payment_type_map, ActionType
from chat.utils import HandlerOption
from chat.register import check_client
from db.banner_db import BannerDB
from db.price_db import PriceDB
from db.product_db import ProductDB
from models.payment_type import PaymentType
from models.status import Status


class RentOptions:
    ACCEPT_RULES = "ACCEPT_RULES"
    DENY_RULES = "DENY_RULES"
    PRODUCT_TYPE = "PRODUCT_TYPE"
    CHOOSE_PRODUCT = "CHOOSE_PRODUCT"
    ACCEPT_PRODUCT = "ACCEPT_PRODUCT"
    DENY_PRODUCT = "DENY_PRODUCT"
    PERIOD = "PERIOD"
    PAYMENT_TYPE = "PAYMENT_TYPE"


async def inline_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    print("[inline_options]")
    print(query.data)
    if query.data.startswith(RentOptions.ACCEPT_RULES):
        return await choose_moped(update, context, query)
    elif query.data.startswith(RentOptions.DENY_RULES):
        await query.edit_message_text(text=f"Заказ отменен ❌\nХорошего вам дня 😉")
        return HandlerOption.ACTION
    elif query.data.startswith(RentOptions.PRODUCT_TYPE):
        return await show_products(update, context, query)
    elif query.data.startswith(RentOptions.CHOOSE_PRODUCT):
        return await show_product_by_number(update, context, query)
    elif query.data.startswith(RentOptions.DENY_PRODUCT):
        return await choose_moped(update, context, query)
    elif query.data.startswith(RentOptions.ACCEPT_PRODUCT):
        return await choose_period(update, context, query)
    elif query.data.startswith(RentOptions.PERIOD):
        return await choose_payment_method(update, context, query)
    elif query.data.startswith(RentOptions.PAYMENT_TYPE):
        context.user_data['rent_data'] = query.data
        title = "Проверка пользователя..."
        await query.edit_message_text(text=title)
        return await check_client(update, context)


async def start_rent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    rules = "Условия аренды мопеда ⬇️\n" \
            "1) Лица старше 18 лет (при себе иметь удв.личности)\n" \
            "2) Знание ПДД\n" \
            "3) Подтверждение работы курьером мин 1 месяц (для курьеров)"

    keyboard = [[InlineKeyboardButton(ActionType.ACCEPT, callback_data=RentOptions.ACCEPT_RULES),
                 InlineKeyboardButton(ActionType.CANCEL, callback_data=RentOptions.DENY_RULES)]]
    await update.message.reply_text(text=rules, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
    return HandlerOption.BOOKING


async def choose_moped(update: Update, context: ContextTypes.DEFAULT_TYPE, query) -> int:
    banners_db = BannerDB()
    banners = banners_db.get_all()
    product_db = ProductDB()
    products = product_db.get_all()
    title = "ВЫБЕРИТЕ МОДЕЛЬ МОПЕДА ⬇️"
    keyboard = []
    for banner in banners:
        print(banner.product_type)
        left_count = 0
        total_count = 0
        for product in products:
            if banner.product_type == product.product_type:
                total_count = total_count + 1
                if product.status == Status.ACTIVE:
                    left_count = left_count + 1
        if left_count != 0:
            keyboard.append([InlineKeyboardButton(banner.model, callback_data=f"{RentOptions.PRODUCT_TYPE}_{banner.product_type}")])

    keyboard.append([InlineKeyboardButton(ActionType.CANCEL, callback_data=RentOptions.DENY_RULES)])
    await query.edit_message_text(text=title, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
    return HandlerOption.BOOKING


async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE, query) -> int:
    product_db = ProductDB()
    products = product_db.get_all()
    product_type = query.data.replace(f"{RentOptions.PRODUCT_TYPE}_", "")
    print(product_type)
    title = "ДОСТУПНЫЕ МОПЕДЫ ⬇️"
    keyboard = []

    filtered_products = []
    for product in products:
        if product.product_type == product_type and product.status == Status.ACTIVE:
            filtered_products.append(product)

    for i in range(0, len(filtered_products), 2):
        product1 = filtered_products[i]
        try:
            product2 = filtered_products[i+1]
            inline_opt1 = InlineKeyboardButton(f"#️⃣ {product1.number}-{product1.model}", callback_data=f"{RentOptions.CHOOSE_PRODUCT}_{product1.number}")
            inline_opt2 = InlineKeyboardButton(f"#️⃣ {product2.number}-{product2.model}", callback_data=f"{RentOptions.CHOOSE_PRODUCT}_{product2.number}")
            keyboard.append([inline_opt1, inline_opt2])
        except:
            inline_opt = InlineKeyboardButton(f"#️⃣ {product1.number}-{product1.model}", callback_data=f"{RentOptions.CHOOSE_PRODUCT}_{product1.number}")
            keyboard.append([inline_opt])

    keyboard.append([InlineKeyboardButton(ActionType.CANCEL, callback_data=RentOptions.DENY_RULES)])
    await query.edit_message_text(text=title, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
    return HandlerOption.BOOKING


async def show_product_by_number(update: Update, context: ContextTypes.DEFAULT_TYPE, query) -> int:
    title = "ВЫ УВЕРЕНЫ ЧТО ХОТИТЕ ВЫБРАТЬ ИМЕННО ЭТОТ МОПЕД?"
    product_db = ProductDB()
    product_number = query.data.replace(f"{RentOptions.CHOOSE_PRODUCT}_", "")
    product = product_db.get_product(product_number)
    for index, image in enumerate(product.images):
        title = title + f"\n{index + 1}) <a href='{image}'>Фотография мопеда</a>"

    keyboard = [[InlineKeyboardButton(ActionType.YES, callback_data=f"{RentOptions.ACCEPT_PRODUCT}_{product.number}"),
                 InlineKeyboardButton(ActionType.NO, callback_data=RentOptions.DENY_PRODUCT)]]
    await query.edit_message_text(text=title, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard), parse_mode=ParseMode.HTML)
    return HandlerOption.BOOKING


async def choose_period(update: Update, context: ContextTypes.DEFAULT_TYPE, query) -> int:
    product_db = ProductDB()
    product_number = query.data.replace(f"{RentOptions.ACCEPT_PRODUCT}_", "")
    product_type = product_db.get_product(product_number).product_type
    prices = PriceDB().get_by_product_type(product_type)
    data = f"{RentOptions.PERIOD}-{product_number}"

    title = "ВЫБЕРИТЕ ПЕРИОД АРЕНДЫ ⬇️"

    keyboard = []
    for price in prices:
        keyboard.append([InlineKeyboardButton(f"{price.text} {'{:0,.2f}'.format(price.price)} ₸", callback_data=f"{data}-{price.period}")])
    keyboard.append([InlineKeyboardButton(ActionType.CANCEL, callback_data=RentOptions.DENY_RULES)])
    await query.edit_message_text(text=title, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard), parse_mode=ParseMode.HTML)
    return HandlerOption.BOOKING


async def choose_payment_method(update: Update, context: ContextTypes.DEFAULT_TYPE, query) -> int:
    query_row = query.data.split('-')

    data = f"{RentOptions.PAYMENT_TYPE}-{query_row[1]}-{query_row[2]}"

    title = "ВЫБЕРИТЕ СПОСОБ ОПЛАТЫ ⬇️"

    keyboard = [
        [
            InlineKeyboardButton(payment_type_map[PaymentType.KASPI_GOLD], callback_data=f"{data}-{PaymentType.KASPI_GOLD}")
        ],
        [
            InlineKeyboardButton(payment_type_map[PaymentType.KASPI_RED], callback_data=f"{data}-{PaymentType.KASPI_RED}")
        ],
        [
            InlineKeyboardButton(payment_type_map[PaymentType.CASH], callback_data=f"{data}-{PaymentType.CASH}")
        ],
        [
            InlineKeyboardButton(ActionType.CANCEL, callback_data=RentOptions.DENY_RULES)
        ]
    ]
    await query.edit_message_text(text=title, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard), parse_mode=ParseMode.HTML)
    return HandlerOption.BOOKING
