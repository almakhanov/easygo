from telegram import Update
from telegram.ext import ContextTypes

from chat.chat_utils import HandlerOption
from chat.complete import complete_rent
from db.client_db import ClientDB


class ClientState:
    IDLE = "IDLE"
    LAST_NAME = "LAST_NAME"
    FIRST_NAME = "FIRST_NAME"
    IIN = "IIN"
    PHONE = "PHONE"
    SECOND_PHONE = "SECOND_PHONE"
    ADDRESS = "ADDRESS"
    PHOTO = "PHOTO"


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


async def enter_last_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    title = "Введите вашу Фамилию ✏️"
    context.user_data['state'] = ClientState.LAST_NAME
    try:
        await update.callback_query.message.reply_text(title)
    except:
        await update.message.reply_text(title)
    return HandlerOption.CLIENT


async def enter_first_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    title = "Введите ваше Имя ✏️"
    context.user_data['state'] = ClientState.FIRST_NAME
    try:
        await update.callback_query.message.reply_text(title)
    except:
        await update.message.reply_text(title)
    return HandlerOption.CLIENT


async def enter_iin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    title = "Введите ваш ИИН ✏️"
    context.user_data['state'] = ClientState.IIN
    try:
        await update.callback_query.message.reply_text(title)
    except:
        await update.message.reply_text(title)
    return HandlerOption.CLIENT


async def enter_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    title = "Введите ваш номер телефона ✏️"
    context.user_data['state'] = ClientState.PHONE
    try:
        await update.callback_query.message.reply_text(title)
    except:
        await update.message.reply_text(title)
    return HandlerOption.CLIENT


async def enter_second_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    title = "Введите номер телефона вашего близкого человека ✏️"
    context.user_data['state'] = ClientState.SECOND_PHONE
    try:
        await update.callback_query.message.reply_text(title)
    except:
        await update.message.reply_text(title)
    return HandlerOption.CLIENT


async def enter_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    title = "Введите ваш адрес дома ✏️"
    context.user_data['state'] = ClientState.ADDRESS
    try:
        await update.callback_query.message.reply_text(title)
    except:
        await update.message.reply_text(title)
    return HandlerOption.CLIENT
