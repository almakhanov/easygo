from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, \
    CallbackQueryHandler, PicklePersistence

from chat.admin import start_admin_panel, run_admin
from chat.banners import show_price
from chat.booking import start_rent, inline_options
from chat.utils import main_keyboard, ActionType
from chat.register import message_handler, ClientState
from chat.contacts import show_contacts
from chat.help import show_help_options, run_help
from db.admin_db import AdminDB
from db.client_db import ClientDB
from models.client import Client
from chat.utils import HandlerOption
from utils.constants import TOKEN


def init_bot() -> None:
    persistence = PicklePersistence(filepath="persistence")
    application = Application.builder().token(TOKEN).persistence(persistence).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            HandlerOption.ACTION: [MessageHandler(filters.TEXT, run_action)],
            HandlerOption.HELP: [MessageHandler(filters.TEXT, run_help)],
            HandlerOption.BOOKING: [CallbackQueryHandler(inline_options)],
            HandlerOption.CLIENT: [MessageHandler(filters.TEXT, message_handler)],
            HandlerOption.ADMIN: [MessageHandler(filters.TEXT, run_admin)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        name="global",
        persistent=True
    )

    application.add_handler(conv_handler)
    application.run_polling()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    admins_objs = AdminDB().get_all()
    for admin in admins_objs:
        if update.effective_chat.id.__str__() == admin.chat_id:
            context.user_data["admin_data"] = admin
            return await start_admin_panel(update, context)
    return await start_client_panel(update, context)


async def start_client_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = f"Привет {update.effective_user.full_name}!\n\n" \
           f"Я телеграм бот компании EasyGo. " \
           f"Мы занимаемся арендой мопедов в городе Астана."
    await update.message.reply_text(
        text=text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=main_keyboard,
            one_time_keyboard=False,
            input_field_placeholder="Выберите действие"
        )
    )
    client = Client(chat_id=update.effective_chat.id, username=update.effective_user.username)
    client_db = ClientDB()
    client_db.insert_client(client)
    context.user_data['state'] = ClientState.IDLE
    return HandlerOption.ACTION


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


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    await update.message.reply_text(
        f"Bye {user.name}! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END
