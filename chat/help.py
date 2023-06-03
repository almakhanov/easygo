from telegram import Update, ReplyKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from chat.chat_start import main_keyboard
from chat.chat_utils import HandlerOption


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
    return HandlerOption.HELP


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
    return HandlerOption.ACTION
