import logging
import os
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

SUPPORT_MESSAGE = 0

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
    "<b>🤖 Demo Telegram Bot</b>\n\n"
    "Этот бот создан как <b>пример работы</b> разработчика Telegram-ботов.\n\n"
    "Он показывает возможные элементы будущего проекта:\n"
    "• главное меню\n"
    "• навигацию через кнопки\n"
    "• формы заявок\n"
    "• информационные разделы\n"
    "• структуру админ-логики\n\n"
    "<i>Этот бот используется только как демонстрация функционала.</i>"
)

FEATURES_TEXT = (
    "<b>🧰 Возможности</b>\n\n"
    "• многоуровневое меню\n"
    "• каталог товаров и карточки\n"
    "• формы заявок\n"
    "• сценарии заказа\n"
    "• уведомления админу\n"
    "• роли и админ-разделы\n"
    "• интеграции с API / CRM / таблицами\n"
    "• оформление под бренд клиента\n\n"
    "<i>Этот раздел показывает, какие функции могут быть реализованы в реальном проекте.</i>"
)

SHOP_TEXT = (
    "<b>🛍 Демо магазин</b>\n\n"
    "Это пример витрины товаров внутри Telegram-бота.\n"
    "Ниже можно открыть демо-карточки товаров и посмотреть возможный сценарий магазина."
)

ADMIN_TEXT = (
    "<b>🖥 Демо админ-панель</b>\n\n"
    "Пример разделов, которые можно реализовать для администратора:\n\n"
    "• новые заявки\n"
    "• список заказов\n"
    "• управление товарами\n"
    "• рассылка\n"
    "• статистика\n"
    "• управление контентом\n\n"
    "<i>Это демонстрация структуры админской части.</i>"
)

CASES_TEXT = (
    "<b>📁 Кейсы / примеры сценариев</b>\n\n"
    "<b>1. Бот-магазин</b>\n"
    "Каталог, карточка товара, корзина, заявка.\n\n"
    "<b>2. Бот для услуг</b>\n"
    "Презентация услуг, форма обращения, передача заявки админу.\n\n"
    "<b>3. Внутренний бот</b>\n"
    "Роли, доступы, простая админ-панель, уведомления.\n\n"
    "<b>4. Бот с оплатой</b>\n"
    "Счёт, оплата, выдача результата, статусы заказа."
)

ABOUT_TEXT = (
    "<b>ℹ️ О проекте</b>\n\n"
    "Этот Telegram-бот создан как часть портфолио разработчика.\n\n"
    "Цель бота — показать возможную структуру и интерфейс будущих проектов.\n\n"
    "В демонстрации реализованы:\n"
    "• меню и навигация\n"
    "• формы заявок\n"
    "• информационные блоки\n"
    "• пример админ-уведомлений\n\n"
    "Бот используется исключительно как демонстрационный пример."
)

CONTACT_TEXT = (
    "<b>📨 Демонстрация формы</b>\n\n"
    "Этот раздел показывает пример формы обращения пользователя.\n"
    "В реальном проекте здесь можно реализовать связь с менеджером или поддержкой."
)


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
    )


def back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🏠 На главный экран", callback_data="show_home")],
        ]
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name or 'друг'}! 👋\n\n"
        "Это демонстрационный бот-портфолио. "
        "Он показывает, как могут выглядеть разные экраны и сценарии внутри Telegram.",
        reply_markup=MAIN_MENU,
    )
    await show_home_message(update.message)


async def show_home_message(target_message) -> None:
    frames = [
        "<b>✨ Главный экран</b>\n\n▰▱▱ Загрузка интерфейса...",
        "<b>✨ Главный экран</b>\n\n▰▰▱ Подготовка разделов...",
        "<b>✨ Главный экран</b>\n\n▰▰▰ Готово.",
    ]
    for frame in frames:
        await target_message.reply_text(frame, parse_mode=ParseMode.HTML)

    await target_message.reply_text(
        HERO_TEXT,
        parse_mode=ParseMode.HTML,
        reply_markup=landing_keyboard(),
    )


async def menu_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()

    if text == "✨ Главный экран":
        await show_home_message(update.message)
        return ConversationHandler.END

    if text == "🛍 Демо магазин":
        await update.message.reply_text(
            SHOP_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=shop_keyboard(),
        )
        return ConversationHandler.END

    if text == "🧰 Возможности":
        await update.message.reply_text(
            FEATURES_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=back_keyboard(),
        )
        return ConversationHandler.END

    if text == "🖥 Демо админ-панель":
        await update.message.reply_text(
            ADMIN_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=admin_keyboard(),
        )
        return ConversationHandler.END

    if text == "📁 Кейсы":
        await update.message.reply_text(
            CASES_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=back_keyboard(),
        )
        return ConversationHandler.END

    if text == "📨 Демо форма":
        await update.message.reply_text(CONTACT_TEXT, parse_mode=ParseMode.HTML)
        await update.message.reply_text(
            "Напиши любое сообщение, чтобы увидеть пример обработки формы."
        )
        return SUPPORT_MESSAGE

    if text == "ℹ️ О проекте":
        await update.message.reply_text(
            ABOUT_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=back_keyboard(),
        )
        return ConversationHandler.END

    await update.message.reply_text(
        "Выбери нужный раздел в меню 👇",
        reply_markup=MAIN_MENU,
    )
    return ConversationHandler.END


async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    product_cards = {
        "product_1": (
            "<b>📦 Товар 1</b>\n\n"
            "Пример карточки товара:\n"
            "• изображение / обложка\n"
            "• описание\n"
            "• цена\n"
            "• кнопка заказа\n\n"
            "<i>Используется как демонстрация магазина.</i>"
        ),
        "product_2": (
            "<b>🎧 Товар 2</b>\n\n"
            "Пример другой карточки товара с кратким описанием и кнопками.\n\n"
            "<i>Можно адаптировать под цифровые товары или услуги.</i>"
        ),
        "product_3": (
            "<b>💎 Товар 3</b>\n\n"
            "Карточка премиум-позиции: акцент на визуал, преимущества и сценарий оформления.\n\n"
            "<i>Подходит для витрины услуг.</i>"
        ),
        "admin_leads": (
            "<b>📥 Новые заявки</b>\n\n"
            "• Иван — бот-магазин\n"
            "• Анна — бот услуг\n"
            "• Максим — бот с оплатой\n\n"
            "<i>Демо списка заявок в админке.</i>"
        ),
        "admin_stats": (
            "<b>📊 Статистика</b>\n\n"
            "• Пользователей: 128\n"
            "• Заявок: 17\n"
            "• Повторных обращений: 6\n\n"
            "<i>Пример экрана аналитики.</i>"
        ),
        "admin_broadcast": (
            "<b>📣 Рассылка</b>\n\n"
            "Здесь может быть создание текста рассылки, выбор сегмента и запуск отправки.\n\n"
            "<i>Демо-экран инструмента администратора.</i>"
        ),
    }

    if query.data == "show_shop":
        await query.message.reply_text(
            SHOP_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=shop_keyboard(),
        )
        return

    if query.data == "show_admin":
        await query.message.reply_text(
            ADMIN_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=admin_keyboard(),
        )
        return

    if query.data == "show_cases":
        await query.message.reply_text(
            CASES_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=back_keyboard(),
        )
        return

    if query.data == "show_home":
        await show_home_message(query.message)
        return

    if query.data in product_cards:
        await query.message.reply_text(
            product_cards[query.data],
            parse_mode=ParseMode.HTML,
            reply_markup=back_keyboard(),
        )
        return


async def support_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()

    await update.message.reply_text(
        "<b>📩 Сообщение отправлено</b>\n\n"
        f"{text}\n\n"
        "В рабочей версии это сообщение может отправляться админу, менеджеру или в CRM.",
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
    app.add_handler(
        CallbackQueryHandler(
            callback_router,
            pattern=r"^(show_shop|show_admin|show_cases|show_home|product_1|product_2|product_3|admin_leads|admin_stats|admin_broadcast)$",
        )
    )
    app.add_handler(support_conversation)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_router))

    logger.info("Demo bot started")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
