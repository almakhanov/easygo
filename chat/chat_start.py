from datetime import datetime, timedelta

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, \
    CallbackQueryHandler
import requests

from db.banner_db import BannerDB
from db.client_db import ClientDB
from db.price_db import PriceDB
from db.product_db import ProductDB
from db.rent_db import RentDB
from models.client import Client
from models.payment_type import PaymentType
from models.period import Period
from models.rent import Rent
from models.rent_status import RentStatus
from models.status import Status
from utils.constants import TOKEN, ADMINS


def init_bot() -> None:
    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ACTION: [MessageHandler(filters.TEXT, run_action)],
            HELP: [MessageHandler(filters.TEXT, run_help)],
            BOOKING: [CallbackQueryHandler(inline_options)],
            CLIENT: [MessageHandler(filters.TEXT, message_handler)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()


# Main Menu Responses
ACTION, HELP, BOOKING, CLIENT = range(4)


class ActionType:
    RENT = "Арендовать 🛵"
    PRICE = "Цены 💰"
    CONTACTS = "Контакты ☎️"
    HELP = "Помощь 🆘"
    ACCEPT = "Принимаю ✅"
    CANCEL = "Отмена ❌"
    YES = "Да 👍"
    NO = "Нет 👎"


class HelpOptions:
    HELP0 = "🗒 Какие условия аренды?"
    HELP1 = "🔑 Что делать если мопед не заводится?"
    HELP2 = "🚓 Что делать если попал в ДТП?"
    HELP3 = "⚙️ Что делать если сломал мопед?"
    HELP4 = "⏰ Что будет если вовремя не возвращать мопед?"
    HELP5 = "👀 Где можно оставлять мопед?"
    HELP6 = "🔴 Могу ли я брать мопед по Kaspi Red?"
    HELP7 = "🥷 Что если украли мопед?"
    HELP8 = "💵 Какие цены на запчасти?"
    HELP9 = "🚪 Выход"


class ClientState:
    IDLE = "IDLE"
    LAST_NAME = "LAST_NAME"
    FIRST_NAME = "FIRST_NAME"
    IIN = "IIN"
    PHONE = "PHONE"
    SECOND_PHONE = "SECOND_PHONE"
    ADDRESS = "ADDRESS"
    PHOTO = "PHOTO"


main_keyboard = [[ActionType.RENT, ActionType.PRICE], [ActionType.CONTACTS, ActionType.HELP]]
payment_type_map = {
    PaymentType.KASPI_GOLD: "Оплата с KaspiQR 🤳",
    PaymentType.KASPI_RED: "Kaspi Red 🔴",
    PaymentType.CASH: "Наличными/Перевод 💵"
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        f"Привет {update.effective_user.full_name}!\n\n"
        "Я телеграм бот компании EasyGo. "
        "Мы занимаемся арендой мопедов в городе Астана.",
        reply_markup=ReplyKeyboardMarkup(
            main_keyboard, one_time_keyboard=False, input_field_placeholder="Выберите действие"
        ),
    )
    client = Client(chat_id=update.effective_chat.id, username=update.effective_user.username)
    client_db = ClientDB()
    client_db.insert_client(client)
    context.user_data['state'] = ClientState.IDLE
    return ACTION


async def run_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    action = update.message.text
    match action:
        case ActionType.RENT:
            return await start_rent(update, context)

        case ActionType.PRICE:
            return show_price(update, context)

        case ActionType.CONTACTS:
            return await show_contacts(update, context)

        case ActionType.HELP:
            return await show_help_options(update, context)


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
        return await query.edit_message_text(text=f"Заказ отменен ❌\nХорошего вам дня 😉")
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
    return BOOKING


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
    return BOOKING


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
    return BOOKING


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
    return BOOKING


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
    return BOOKING


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
    return BOOKING


async def check_client(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    client_db = ClientDB()
    client = client_db.get_client(update.effective_chat.id.__str__())
    if client.lastname is None:
        return await enter_last_name(update, context)
    elif client.firstname is None:
        return await enter_first_name(update, context)
    elif client.iin is None:
        return await enter_iin(update, context)
    elif client.phone is None:
        return await enter_phone(update, context)
    elif client.second_phone is None:
        return await enter_second_phone(update, context)
    elif client.address is None:
        return await enter_address(update, context)
    else:
        context.user_data['state'] = ClientState.IDLE
        return await complete_rent(update, context)


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

    for admin in ADMINS:
        try:
            req_body = f'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + admin + '&parse_mode=HTML&text=' + title
            resp = requests.get(req_body)
            print(resp.content)
        except Exception as e:
            print(e)

    try:
        await update.callback_query.message.reply_text(title, parse_mode=ParseMode.HTML)
    except:
        await update.message.reply_text(title, parse_mode=ParseMode.HTML)
    return ACTION


async def enter_last_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    title = "Введите вашу Фамилию ✏️"
    context.user_data['state'] = ClientState.LAST_NAME
    try:
        await update.callback_query.message.reply_text(title)
    except:
        await update.message.reply_text(title)
    return CLIENT


async def enter_first_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    title = "Введите ваше Имя ✏️"
    context.user_data['state'] = ClientState.FIRST_NAME
    try:
        await update.callback_query.message.reply_text(title)
    except:
        await update.message.reply_text(title)
    return CLIENT


async def enter_iin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    title = "Введите ваш ИИН ✏️"
    context.user_data['state'] = ClientState.IIN
    try:
        await update.callback_query.message.reply_text(title)
    except:
        await update.message.reply_text(title)
    return CLIENT


async def enter_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    title = "Введите ваш номер телефона ✏️"
    context.user_data['state'] = ClientState.PHONE
    try:
        await update.callback_query.message.reply_text(title)
    except:
        await update.message.reply_text(title)
    return CLIENT


async def enter_second_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    title = "Введите номер телефона вашего близкого человека ✏️"
    context.user_data['state'] = ClientState.SECOND_PHONE
    try:
        await update.callback_query.message.reply_text(title)
    except:
        await update.message.reply_text(title)
    return CLIENT


async def enter_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    title = "Введите ваш адрес дома ✏️"
    context.user_data['state'] = ClientState.ADDRESS
    try:
        await update.callback_query.message.reply_text(title)
    except:
        await update.message.reply_text(title)
    return CLIENT


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("[message_handler]")
    print(update.effective_chat.id)
    try:
        print(context.user_data['state'])
    except:
        context.user_data['state'] = ClientState.IDLE

    if context.user_data['state'] != ClientState.IDLE:
        client_db = ClientDB()
        client = client_db.get_client(update.effective_chat.id.__str__())
        match context.user_data['state']:
            case ClientState.LAST_NAME:
                client.lastname = update.message.text
            case ClientState.FIRST_NAME:
                client.firstname = update.message.text
            case ClientState.IIN:
                client.iin = update.message.text
            case ClientState.PHONE:
                client.phone = update.message.text
            case ClientState.SECOND_PHONE:
                client.second_phone = update.message.text
            case ClientState.ADDRESS:
                client.address = update.message.text

        print(client)
        client_db.update_client(client)
        return await check_client(update, context)


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
    return ACTION


async def show_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    address = "Наш адрес: <a href='https://2gis.kz/astana/geo/9570784863354424'>г. Астана, ул. Улы дала, дом 62</a>"
    contacts = "Тел. номер: [+77022021399](tel:+77022021399)" \
               "\n\nДоп. номер: [+77779565737](tel:+77779565737)" \
               "\n\nИнженер: [+77477314023](tel:+77477314023)"
    await update.message.reply_text(text=address, parse_mode=ParseMode.HTML)
    await update.message.reply_text(text=contacts, parse_mode=ParseMode.MARKDOWN)
    return ACTION


async def show_help_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [[HelpOptions.HELP0], [HelpOptions.HELP1], [HelpOptions.HELP2], [HelpOptions.HELP3],
                      [HelpOptions.HELP4], [HelpOptions.HELP5], [HelpOptions.HELP7], [HelpOptions.HELP8],
                      [HelpOptions.HELP9]]
    await update.message.reply_text(
        "Чем я могу быть вам полезен?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Ваш вопрос"
        ),
    )
    return HELP


async def run_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    help_option = update.message.text
    reply_text = ""
    match help_option:
        case HelpOptions.HELP0:
            reply_text = "Условия аренды мопеда!\n" \
                         "1) Лица старше 18 лет (при себе иметь удв.личности)\n" \
                         "2) Знание ПДД\n" \
                         "3) Подтверждение работы курьером мин 1 месяц (для курьеров)\n" \
                         "4) Подписание договора\n" \
                         "5) Эксплуатация мопеда в пределах города Астана\n" \
                         "6) Иметь безопасное месторасположение для парковки мопеда на ночь. К безопасным местам относится:\n" \
                         "\t- частный дом;\n" \
                         "\t- собственная парковка;\n" \
                         "\t- охраняемое ЖК с камерами, охраной, забором где не будет возможности унести мопед без ключа домофона. Не оставлять возле подьезда;\n" \
                         "7) Гражданин РК"

        case HelpOptions.HELP1:
            reply_text = f"1) Вызовите грузовик через “Яндекс Go” до <a href='https://2gis.kz/astana/geo/9570784863354424'>Улы Дала 62, гараж 9</a> (Опций: Без грузчика; Маленький кузов. Оплатим грузовик за свой счёт, после отправки скрина вызова грузовика). Мы сделаем замену мопеда.\n" \
                         f"2) Если у Вас <b>ВО ВРЕМЯ ЗАКАЗА</b> не заводится мопед, то вызовите доставку до адреса Вашего заказа (оплатим доставку за свой счёт, после отправки скрина вызова доставки и адреса доставки с приложения Glovo/Wolt/Яндекс).  "

        case HelpOptions.HELP2:
            reply_text = f"Без паники. Звоните на номера:\n" \
                         f"1) +77022021399\n" \
                         f"2) +77779565737"

        case HelpOptions.HELP3:
            reply_text = f"Если мопед сломан по Вашей вине, то у Вас два выбора:\n" \
                         f"1) Вы оплачиваете штраф за повреждение согласно договору\n" \
                         f"2) Вы чините мопед сами. Находите техника, спец. СТО. Ставить качественные запчасти! Продлеваете аренду если не успеваете с ремонтом\n\n" \
                         f"PS. Если вы считаете, что мопед не был сломан по Вашей вине и это подтвердит мастер, то мы Вам сделаем замену мопеда"

        case HelpOptions.HELP4:
            reply_text = f"Ежедневный штраф по дневному тарифному плану 7000 тг."

        case HelpOptions.HELP5:
            reply_text = f"Безопасные места:\n" \
                         f"1) Частный дом\n" \
                         f"2) Cобственная парковка\n" \
                         f"3) Охраняемое ЖК с камерами, охраной, забором где не будет возможности унести мопед без ключа домофона. Не оставлять возле подьезда"

        case HelpOptions.HELP6:
            reply_text = f"Да, цена с Kaspi Red = Цена + Комиссия банка (12.5%)"

        case HelpOptions.HELP7:
            reply_text = f"Оплачиваете сумму указанную по договору за мопед – 440 000 ₸"

        case HelpOptions.HELP8:
            reply_text = f"Цены на запчасти:\n" \
                         f"- Боковой обтекатель: 36 000 ₸\n" \
                         f"- Передний парус: 18 000 ₸\n" \
                         f"- Передняя накладка: 20 000 ₸\n" \
                         f"- Окантовка фары: 12 000 ₸\n" \
                         f"- Пластик руля (2 части): 36 000 ₸\n" \
                         f"- Фара: 8 500 ₸\n" \
                         f"- Стоп-сигнал в сборе: 14 000 ₸\n" \
                         f"- Ручка газа: 8 500 ₸\n" \
                         f"- Колесный диск: 12 000 ₸\n" \
                         f"- Крыло переднее: 36 000 ₸\n" \
                         f"- Кнопка, переключатель: 3 600 ₸\n" \
                         f"- Зеркала комплект: 6 000 ₸\n" \
                         f"- Ключ: 12 000 ₸\n" \
                         f"- Покрышка: 14 000 ₸\n" \
                         f"- Глушитель: 24 000 ₸\n" \
                         f"- Чехол сидения: 18 000 ₸\n" \
                         f"- Шлем: 9 000 ₸"

        case HelpOptions.HELP9:
            reply_text = f"Если вы не нашли вопрос который вас волнует, наберите нас по номеру указанной в пункте <b>Контакты ☎️</b>"

    print(reply_text)
    await update.message.reply_text(
        reply_text,
        reply_markup=ReplyKeyboardMarkup(
            main_keyboard, one_time_keyboard=False, input_field_placeholder="Выберите действие"
        ),
        parse_mode=ParseMode.HTML
    )
    return ACTION


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    await update.message.reply_text(
        f"Bye {user.name}! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END
