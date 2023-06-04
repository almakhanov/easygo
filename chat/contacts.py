from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from chat.utils import HandlerOption


async def show_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    address = "Наш адрес: <a href='https://2gis.kz/astana/geo/9570784863354424'>г. Астана, ул. Улы дала, дом 62</a>"
    contacts = "Тел. номер: [+77022021399](tel:+77022021399)" \
               "\n\nДоп. номер: [+77779565737](tel:+77779565737)" \
               "\n\nИнженер: [+77477314023](tel:+77477314023)"
    await update.message.reply_text(text=address, parse_mode=ParseMode.HTML)
    await update.message.reply_text(text=contacts, parse_mode=ParseMode.MARKDOWN)
    return HandlerOption.ACTION
