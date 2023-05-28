from requests import Response
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, \
    CallbackQueryHandler
import requests

from db.banner_db import BannerDB
from db.client_db import ClientDB
from db.product_db import ProductDB
from models.status import Status
from utils.constants import TOKEN


def init_bot() -> None:
    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ACTION: [MessageHandler(filters.TEXT, run_action)],
            HELP: [MessageHandler(filters.TEXT, run_help)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(inline_options))
    application.run_polling()


# Main Menu Responses
ACTION, HELP = range(2)


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


main_keyboard = [[ActionType.RENT, ActionType.PRICE], [ActionType.CONTACTS, ActionType.HELP]]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        f"Привет {update.effective_user.full_name}!\n\n"
        "Я телеграм бот компании EasyGo. "
        "Мы занимаемся арендой мопедов в городе Астана.",
        reply_markup=ReplyKeyboardMarkup(
            main_keyboard, one_time_keyboard=False, input_field_placeholder="Выберите действие"
        ),
    )

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


async def inline_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    print(query)
    print(query.message)
    print(query.data)
    if query.data.startswith(RentOptions.ACCEPT_RULES):
        await choose_moped(update, context, query)
    elif query.data.startswith(RentOptions.DENY_RULES):
        await query.edit_message_text(text=f"Заказ отменен ❌\nХорошего вам дня 😉")
    elif query.data.startswith(RentOptions.PRODUCT_TYPE):
        await show_products(update, context, query)
    elif query.data.startswith(RentOptions.CHOOSE_PRODUCT):
        await show_product_by_number(update, context, query)
    elif query.data.startswith(RentOptions.DENY_PRODUCT):
        await choose_moped(update, context, query)


async def start_rent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    rules = "Условия аренды мопеда ⬇️\n" \
            "1) Лица старше 18 лет (при себе иметь удв.личности)\n" \
            "2) Знание ПДД\n" \
            "3) Подтверждение работы курьером мин 1 месяц (для курьеров)"

    keyboard = [[InlineKeyboardButton(ActionType.ACCEPT, callback_data=RentOptions.ACCEPT_RULES),
                 InlineKeyboardButton(ActionType.CANCEL, callback_data=RentOptions.DENY_RULES)]]
    await update.message.reply_text(text=rules, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
    return ACTION


async def choose_moped(update: Update, context: ContextTypes.DEFAULT_TYPE, query) -> None:
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


async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE, query) -> None:
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


async def show_product_by_number(update: Update, context: ContextTypes.DEFAULT_TYPE, query) -> None:
    title = "ВЫ УВЕРЕНЫ ЧТО ХОТИТЕ ВЫБРАТЬ ИМЕННО ЭТОТ МОПЕД?"
    product_db = ProductDB()
    product_number = query.data.replace(f"{RentOptions.CHOOSE_PRODUCT}_", "")
    product = product_db.get_product(product_number)
    for index, image in enumerate(product.images):
        title = title + f"\n{index + 1}) <a href='{image}'>Фотография мопеда</a>"

    keyboard = [[InlineKeyboardButton(ActionType.YES, callback_data=f"{RentOptions.ACCEPT_PRODUCT}_{product.number}"),
                 InlineKeyboardButton(ActionType.NO, callback_data=RentOptions.DENY_PRODUCT)]]
    await query.edit_message_text(text=title, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard), parse_mode=ParseMode.HTML)


async def check_client(update: Update, context: ContextTypes.DEFAULT_TYPE, number) -> None:
    await update.message.reply_text(text=f"{update.effective_user.full_name}")


def show_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    banner_db = BannerDB()
    product_db = ProductDB()
    banners = banner_db.get_all()
    products = product_db.get_all()

    for banner in banners:
        print(banner.product_type)
        left_count = 0
        total_count = 0
        for product in products:
            if banner.product_type == product.product_type:
                total_count = total_count + 1
                if product.status == Status.ACTIVE:
                    left_count = left_count + 1
        banner.left_count = left_count
        banner.total_count = total_count

    for banner in banners:
        resp = None
        try:
            resp = requests.get(
                f'https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={update.effective_chat.id}&caption={banner}&photo={banner.image}')
        except:
            print(resp)
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
                      [HelpOptions.HELP4], [HelpOptions.HELP5], [HelpOptions.HELP7], [HelpOptions.HELP8]]
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
                         "3) Подтверждение работы курьером мин 1 месяц (для курьеров)"

        case HelpOptions.HELP1:
            reply_text = f"HelpOptions.HELP1"

        case HelpOptions.HELP2:
            reply_text = f"HelpOptions.HELP2"

        case HelpOptions.HELP3:
            reply_text = f"HelpOptions.HELP3"

        case HelpOptions.HELP4:
            reply_text = f"HelpOptions.HELP4"

        case HelpOptions.HELP5:
            reply_text = f"HelpOptions.HELP5"

        case HelpOptions.HELP6:
            reply_text = f"HelpOptions.HELP6"

        case HelpOptions.HELP7:
            reply_text = f"HelpOptions.HELP7"

        case HelpOptions.HELP8:
            reply_text = f"HelpOptions.HELP7"

    print(reply_text)
    await update.message.reply_text(
        reply_text,
        reply_markup=ReplyKeyboardMarkup(
            main_keyboard, one_time_keyboard=False, input_field_placeholder="Выберите действие"
        )
    )
    return ACTION


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    await update.message.reply_text(
        f"Bye {user.name}! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END
