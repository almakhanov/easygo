from models.payment_type import PaymentType


class HandlerOption:
    ACTION = 0
    HELP = 1
    BOOKING = 2
    CLIENT = 3
    ADMIN = 4


class ActionType:
    RENT = "Арендовать 🛵"
    PRICE = "Цены 💰"
    CONTACTS = "Контакты ☎️"
    HELP = "Помощь 🆘"
    ACCEPT = "Принимаю ✅"
    CANCEL = "Отмена ❌"
    YES = "Да 👍"
    NO = "Нет 👎"


main_keyboard = [[ActionType.RENT, ActionType.PRICE], [ActionType.CONTACTS, ActionType.HELP]]


payment_type_map = {
    PaymentType.KASPI_GOLD: "KaspiQR 🤳",
    PaymentType.KASPI_RED: "Kaspi Red 🔴",
    PaymentType.CASH: "Наличными 💵"
}
