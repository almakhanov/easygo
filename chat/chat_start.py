from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
import requests

from db.banner_db import BannerDB
from db.client_db import ClientDB
from db.product_db import ProductDB
from models.status import Status
from utils.constants import TOKEN


def init_bot() -> None:
    application = Application.builder().token(TOKEN).build()
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ACTION: [MessageHandler(filters.TEXT, run_action)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("mopeds", mopeds))
    application.run_polling()


ACTION, RENT, PRODUCT, CONTACTS, HELP = range(5)


class ActionType:
    RENT = "Арендовать 🛵"
    PRICE = "Цены 💰"
    CONTACTS = "Контакты ☎️"
    HELP = "Помощь 🆘"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [[ActionType.RENT, ActionType.PRICE], [ActionType.CONTACTS, ActionType.HELP]]

    await update.message.reply_text(
        f"Привет {update.effective_user.full_name}!\n\n"
        "Я телеграм бот компании EasyGo. "
        "Мы занимаемся арендой мопедов в городе Астана.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Выберите действие"
        ),
    )

    return ACTION


async def run_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    action = update.message.text
    message = "dodo"
    match action:
        case ActionType.RENT:
            start_rent(update, context)

        case ActionType.PRICE:
            show_price(update, context)

        case ActionType.CONTACTS:
            contacts = "Наш адрес: г. Астана, ул. Улы дала, дом 62" \
                       "\n\nТел. номер: [+77022021399](tel:+77022021399)" \
                       "\n\nДоп. номер: [+77779565737](tel:+77779565737)" \
                       "\n\nИнженер: [+77477314023](tel:+77477314023)"
            await update.message.reply_text(contacts, ParseMode.MARKDOWN)

        case ActionType.HELP:
            message = 4


def start_rent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    client_db = ClientDB()



def show_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
        telegram_msg = requests.get(f'https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={update.effective_chat.id}&caption={banner}&photo={banner.image}')
        print(telegram_msg.content)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    await update.message.reply_text(
        f"Bye {user.name}! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def mopeds(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    product_db = ProductDB()
    products = product_db.get_all()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{products[0]}")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)
