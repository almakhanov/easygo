from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from chat.utils import HandlerOption


class AdminAction:
    CANCEL = "Отмена ❌"
    STATUS = "Статусы 🚦"
    MOPEDS = "Мопеды 🛵"
    REPORT = "Отчет 🗒"
    STATISTICS = "Статистика 📊"
    CLIENTS = "Клиенты 👷"
    SETTINGS = "Найтройки ⚙️"

# ACTIVE_PRODUCTS = "Активные мопеды 🚴‍♀️"
#     AVAILABLE_PRODUCTS = "Доступные мопеды 🛵"
#     UNAVAILABLE_PRODUCTS = "Недоступные мопеды ⚙️"
#     ALL_PRODUCTS = "Все мопеды 🍟"
# WAITING = "Заказы в ожидании 📬"
#     RETURN_TODAY = "Сегодня кто возвращает ⏰"
#     LATE_CLIENTS = "Кто опаздывает ⌛️"


admin_keyboard = [
    [AdminAction.STATUS, AdminAction.MOPEDS],
    [AdminAction.REPORT, AdminAction.STATISTICS],
    [AdminAction.CLIENTS, AdminAction.SETTINGS]
]


async def start_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    admin_data = context.user_data["admin_data"]
    text = f"Доброго дня вам мой господин!\n\n" \
           f"Чем я могу быть вам полезен {admin_data.name}?"
    await update.message.reply_text(
        text=text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=admin_keyboard,
            one_time_keyboard=False,
            input_field_placeholder="Выберите действие"
        )
    )
    return HandlerOption.ADMIN


async def run_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    action = update.message.text
    match action:
        case AdminAction.STATUS:
            return HandlerOption.ADMIN

        case AdminAction.MOPEDS:
            return HandlerOption.ADMIN

        case AdminAction.REPORT:
            return HandlerOption.ADMIN

        case AdminAction.STATISTICS:
            return HandlerOption.ADMIN

        case AdminAction.CLIENTS:
            return HandlerOption.ADMIN

        case AdminAction.SETTINGS:
            return HandlerOption.ADMIN
