import logging
import os
from dataclasses import dataclass
from typing import Final

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN: Final[str | None] = os.getenv("BOT_TOKEN")
ADMIN_ID: Final[int] = int(os.getenv("ADMIN_ID", "0"))
FUNPAY_URL: Final[str] = "https://funpay.com/lots/offer?id=65716149"  # ссылка оставлена только как пример портфолио

ASK_NAME, ASK_CONTACT, ASK_PROJECT, SUPPORT_MESSAGE = range(4)

MAIN_MENU = ReplyKeyboardMarkup(
    [
        ["✨ Главный экран", "🛍 Демо магазин"],
        ["🧰 Возможности", "🖥 Демо админ-панель"],
        ["📁 Кейсы", "📨 Демо форма"],
        ["ℹ️ О проекте"],
    ],
    resize_keyboard=True,
)

HERO_TEXT = (
    "<b>🤖 Demo Telegram Bot</b>

"
    "Этот бот создан как <b>пример работы</b> разработчика Telegram‑ботов.

"
    "Он показывает возможные элементы будущего проекта:"
    "
• главное меню"
    "
• навигацию через кнопки"
    "
• формы заявок"
    "
• информационные разделы"
    "
• структуру админ‑логики

"
    "<i>Этот бот используется только как демонстрация функционала.</i>"
)

PORTFOLIO_TEXT = (
    "<b>📁 Примеры функционала</b>

"
    "<b>1. Telegram‑магазин</b>
"
    "Каталог товаров, карточки, оформление заказа.

"
    "<b>2. Бот для заявок</b>
"
    "Сбор контактов клиентов, анкеты и уведомления.

"
    "<b>3. Бот для услуг</b>
"
    "Прайс, кейсы, запись на услугу.

"
    "<b>4. Бот с оплатой</b>
"
    "Интеграция платежей и автоматические статусы.

"
    "<b>5. Индивидуальная логика</b>
"
    "API, CRM интеграции, базы данных, админ‑панель."
)

FEATURES_TEXT = (
    "<b>🧰 Возможности</b>

"
    "• многоуровневое меню
"
    "• каталог товаров и карточки
"
    "• формы заявок
"
    "• сценарии заказа
"
    "• уведомления админу
"
    "• роли и админ-разделы
"
    "• интеграции с API / CRM / таблицами
"
    "• оформление под бренд клиента

"
    "<i>Этот раздел показывает, какие функции могут быть реализованы в реальном проекте.</i>"
)

SHOP_TEXT = (
    "<b>🛍 Демо магазин</b>

"
    "Это пример витрины товаров внутри Telegram-бота.
"
    "Ниже можно открыть демо-карточки товаров и посмотреть возможный сценарий магазина."
)

ADMIN_TEXT = (
    "<b>🖥 Демо админ-панель</b>

"
    "Пример разделов, которые можно реализовать для администратора:

"
    "• новые заявки
"
    "• список заказов
"
    "• управление товарами
"
    "• рассылка
"
    "• статистика
"
    "• управление контентом

"
    "<i>Это демонстрация структуры админской части.</i>"
)

CASES_TEXT = (
    "<b>📁 Кейсы / примеры сценариев</b>

"
    "<b>1. Бот-магазин</b>
Каталог, карточка товара, корзина, заявка.

"
    "<b>2. Бот для услуг</b>
Презентация услуг, форма обращения, передача заявки админу.

"
    "<b>3. Внутренний бот</b>
Роли, доступы, простая админ-панель, уведомления.

"
    "<b>4. Бот с оплатой</b>
Счёт, оплата, выдача результата, статусы заказа."
)

PRICING_TEXT = (
    "<b>⚙️ Архитектура демо‑бота</b>

"
    "Этот раздел показывает, как может выглядеть структура реального проекта.

"
    "• многоуровневое меню
"
    "• сценарии общения с пользователем
"
    "• сбор данных через формы
"
    "• админ‑уведомления
"
    "• возможность интеграций

"
    "Раздел используется только для демонстрации интерфейса."
)

REVIEWS_TEXT = (
    "<b>🧪 Тестовый раздел</b>

"
    "В реальном проекте здесь могут отображаться:
"
    "• отзывы клиентов
"
    "• кейсы проектов
"
    "• примеры внедрения

"
    "В этом демо‑боте раздел используется только как пример интерфейса."
)

ABOUT_TEXT = (
    "<b>ℹ️ О проекте</b>

"
    "Этот Telegram‑бот создан как часть портфолио разработчика.

"
    "Цель бота — показать возможную структуру и интерфейс будущих проектов.

"
    "В демонстрации реализованы:
"
    "• меню и навигация
"
    "• формы заявок
"
    "• информационные блоки
"
    "• пример админ‑уведомлений

"
    "Бот используется исключительно как демонстрационный пример."
)

CONTACT_TEXT = (
    "<b>📨 Демонстрация формы</b>

"
    "Этот раздел показывает пример формы обращения пользователя.
"
    "В реальном проекте здесь можно реализовать связь с менеджером или поддержкой."
)


@dataclass
class OrderDraft:
    name: str = ""
    contact: str = ""
    project: str = ""


def shop_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📦 Товар 1", callback_data="product_1")],
            [InlineKeyboardButton("🎧 Товар 2", callback_data="product_2")],
            [InlineKeyboardButton("💎 Товар 3", callback_data="product_3")],
        ]
    )


def admin_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📥 Новые заявки", callback_data="admin_leads")],
            [InlineKeyboardButton("📊 Статистика", callback_data="admin_stats")],
            [InlineKeyboardButton("📣 Рассылка", callback_data="admin_broadcast")],
        ]
    )


def landing_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🛍 Открыть демо магазин", callback_data="show_shop")],
            [InlineKeyboardButton("🖥 Открыть админ-панель", callback_data="show_admin")],
            [InlineKeyboardButton("📁 Посмотреть кейсы", callback_data="show_cases")],
        ]
    ) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🛒 Заказать на FunPay", url=FUNPAY_URL)],
            [InlineKeyboardButton("✨ Смотреть портфолио", callback_data="show_portfolio")],
            [InlineKeyboardButton("💎 Посмотреть тарифы", callback_data="show_pricing")],
        ]
    )


def order_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🏠 На главный экран", callback_data="show_home")],
        ]
    ) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🛒 Перейти к заказу", url=FUNPAY_URL)],
        ]
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name or 'друг'}! 👋

"
        "Это демонстрационный бот-портфолио. Он показывает, как могут выглядеть разные экраны и сценарии внутри Telegram.",
        reply_markup=MAIN_MENU,
    )
    await show_home_message(update.message)


async def show_home_message(target_message) -> None:
    frames = [
        "<b>✨ Главный экран</b>

▰▱▱ Загрузка интерфейса...",
        "<b>✨ Главный экран</b>

▰▰▱ Подготовка разделов...",
        "<b>✨ Главный экран</b>

▰▰▰ Готово.",
    ]
    for frame in frames:
        await target_message.reply_text(frame, parse_mode=ParseMode.HTML)
    await target_message.reply_text(HERO_TEXT, parse_mode=ParseMode.HTML, reply_markup=landing_keyboard())


async def menu_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()

    if text == "✨ Главный экран":
        await show_home_message(update.message)
        return ConversationHandler.END

    if text == "🛍 Демо магазин":
        await update.message.reply_text(SHOP_TEXT, parse_mode=ParseMode.HTML, reply_markup=shop_keyboard())
        return ConversationHandler.END

    if text == "🧰 Возможности":
        await update.message.reply_text(FEATURES_TEXT, parse_mode=ParseMode.HTML, reply_markup=order_keyboard())
        return ConversationHandler.END

    if text == "🖥 Демо админ-панель":
        await update.message.reply_text(ADMIN_TEXT, parse_mode=ParseMode.HTML, reply_markup=admin_keyboard())
        return ConversationHandler.END

    if text == "📁 Кейсы":
        await update.message.reply_text(CASES_TEXT, parse_mode=ParseMode.HTML, reply_markup=order_keyboard())
        return ConversationHandler.END

        if text == "🧩 Возможности":
        await update.message.reply_text(FEATURES_TEXT, parse_mode=ParseMode.HTML, reply_markup=order_keyboard())
        return ConversationHandler.END

            if text == "📨 Демо форма":
        await update.message.reply_text(CONTACT_TEXT, parse_mode=ParseMode.HTML)
        await update.message.reply_text("Напиши любое сообщение, чтобы увидеть пример обработки формы.")
        return SUPPORT_MESSAGE

    if text == "ℹ️ О студии":
        await update.message.reply_text(ABOUT_TEXT, parse_mode=ParseMode.HTML, reply_markup=order_keyboard())
        return ConversationHandler.END

        if text == "ℹ️ О проекте":
        await update.message.reply_text(ABOUT_TEXT, parse_mode=ParseMode.HTML, reply_markup=order_keyboard())
        return ConversationHandler.END

    

    await update.message.reply_text("Выбери нужный раздел в меню 👇", reply_markup=MAIN_MENU)
    return ConversationHandler.END


async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    product_cards = {
        "product_1": "<b>📦 Товар 1</b>

Пример карточки товара:
• изображение/обложка
• описание
• цена
• кнопка заказа

<i>Используется как демонстрация магазина.</i>",
        "product_2": "<b>🎧 Товар 2</b>

Пример другой карточки товара с кратким описанием и CTA-кнопками.

<i>Можно адаптировать под цифровые товары или услуги.</i>",
        "product_3": "<b>💎 Товар 3</b>

Карточка премиум-позиции: акцент на визуал, преимущества и сценарий оформления.

<i>Подходит для витрины услуг.</i>",
        "admin_leads": "<b>📥 Новые заявки</b>

• Иван — бот-магазин
• Анна — бот услуг
• Максим — бот с оплатой

<i>Демо списка заявок в админке.</i>",
        "admin_stats": "<b>📊 Статистика</b>

• Пользователей: 128
• Заявок: 17
• Повторных обращений: 6

<i>Пример экрана аналитики.</i>",
        "admin_broadcast": "<b>📣 Рассылка</b>

Здесь может быть создание текста рассылки, выбор сегмента и запуск отправки.

<i>Демо-экран инструмента администратора.</i>",
    }

    if query.data == "show_shop":
        await query.message.reply_text(SHOP_TEXT, parse_mode=ParseMode.HTML, reply_markup=shop_keyboard())
        return
    if query.data == "show_admin":
        await query.message.reply_text(ADMIN_TEXT, parse_mode=ParseMode.HTML, reply_markup=admin_keyboard())
        return
    if query.data == "show_cases":
        await query.message.reply_text(CASES_TEXT, parse_mode=ParseMode.HTML, reply_markup=order_keyboard())
        return
    if query.data == "show_home":
        await show_home_message(query.message)
        return
    if query.data in product_cards:
        await query.message.reply_text(product_cards[query.data], parse_mode=ParseMode.HTML, reply_markup=order_keyboard())
        return


async def support_message(update: Update, context: ContextTypes.DEFAULT_TYPE):(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    await update.message.reply_text(
        "<b>📩 Сообщение отправлено</b>\n\n"
        f"{text}\n\n"
        "В рабочей версии это сообщение отправляется админу, менеджеру или в CRM.",
        parse_mode=ParseMode.HTML,
        reply_markup=MAIN_MENU,
    )
    return ConversationHandler.END





async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Действие отменено.", reply_markup=MAIN_MENU)
    return ConversationHandler.END


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("Set BOT_TOKEN environment variable before launch.")

    app = Application.builder().token(BOT_TOKEN).build()

    support_conversation = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex(r"^📨 Демо форма$"), menu_router)],
        states={
            SUPPORT_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, support_message)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_message=False,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_router, pattern=r"^(show_shop|show_admin|show_cases|show_home|product_1|product_2|product_3|admin_leads|admin_stats|admin_broadcast)$"))
    app.add_handler(support_conversation)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_router))

    logger.info("Studio demo bot started")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
