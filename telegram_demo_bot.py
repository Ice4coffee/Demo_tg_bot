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

# ============================================
# DEMO TELEGRAM BOT FOR PORTFOLIO / FANPAY
# Stack: python-telegram-bot v21+
# ============================================
# Features:
# - Main menu
# - Service catalog demo
# - Fake order flow
# - Support request flow
# - Admin info section
# - Portfolio-friendly structure
#
# Run:
#   pip install python-telegram-bot==21.6
#   export BOT_TOKEN="YOUR_TOKEN"
#   python telegram_demo_bot.py
# ============================================

logging.basicConfig(
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN: Final[str | None] = os.getenv("BOT_TOKEN")
ADMIN_ID: Final[int] = int(os.getenv("ADMIN_ID", "0"))

ASK_NAME, ASK_SERVICE, ASK_DETAILS, SUPPORT_MESSAGE = range(4)

MAIN_MENU = ReplyKeyboardMarkup(
    [
        ["📦 Услуги", "🛒 Оформить заказ"],
        ["💬 Поддержка", "ℹ️ О боте"],
        ["👨‍💼 Админ-панель (демо)"],
    ],
    resize_keyboard=True,
)

SERVICES_TEXT = (
    "<b>Пример каталога услуг</b>\n\n"
    "1. 🤖 Telegram-бот под ключ\n"
    "2. 🛍 Бот-магазин с каталогом\n"
    "3. 📩 Бот заявок / запись\n"
    "4. 💳 Подключение оплаты\n"
    "5. 🧩 Индивидуальный функционал\n\n"
    "Это демо-бот для портфолио. Здесь можно показать логику, кнопки, сценарии и оформление."
)

ABOUT_TEXT = (
    "<b>Демо-бот разработчика Telegram-ботов</b>

"
    "Что можно показать клиенту через такой пример:
"
    "• красивое меню
"
    "• сценарий оформления заказа
"
    "• сбор заявок
"
    "• раздел поддержки
"
    "• основу под админку

"
    "<b>Заказать такого бота:</b>
"
    "https://funpay.com/lots/offer?id=65716149

"
    "Этот бот используется как пример работы для FanPay, портфолио и личных продаж."
)


@dataclass
class OrderDraft:
    name: str = ""
    service: str = ""
    details: str = ""


def catalog_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🤖 Бот под ключ", callback_data="service_turnkey")],
            [InlineKeyboardButton("🛍 Бот-магазин", callback_data="service_shop")],
            [InlineKeyboardButton("📩 Бот заявок", callback_data="service_leads")],
            [InlineKeyboardButton("💳 Бот с оплатой", callback_data="service_payment")],
        ]
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    text = (
        f"Привет, {user.first_name or 'друг'}! 👋\n\n"
        "Я демонстрационный бот. Через меня можно показать клиентам, "
        "как будет выглядеть их будущий Telegram-бот.\n\n"
        "Выбери нужный раздел ниже."
    )
    await update.message.reply_text(text, reply_markup=MAIN_MENU)


async def menu_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()

    if text == "📦 Услуги":
        await update.message.reply_text(
            SERVICES_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=catalog_keyboard(),
        )
        return ConversationHandler.END

    if text == "🛒 Оформить заказ":
        context.user_data["order"] = OrderDraft()
        await update.message.reply_text("Введите ваше имя или ник для заявки:")
        return ASK_NAME

    if text == "💬 Поддержка":
        await update.message.reply_text(
            "Напишите сообщение для поддержки.\n"
            "В реальном проекте оно отправится админу или в CRM."
        )
        return SUPPORT_MESSAGE

    if text == "ℹ️ О боте":
        await update.message.reply_text(ABOUT_TEXT, parse_mode=ParseMode.HTML)
        return ConversationHandler.END

    if text == "👨‍💼 Админ-панель (демо)":
        await update.message.reply_text(
            "<b>Демо админ-панели</b>\n\n"
            "Здесь можно сделать:\n"
            "• просмотр заявок\n"
            "• рассылку\n"
            "• управление каталогом\n"
            "• статистику\n"
            "• ответы пользователям\n\n"
            "Сейчас это демонстрационный раздел для портфолио.",
            parse_mode=ParseMode.HTML,
        )
        return ConversationHandler.END

    await update.message.reply_text("Выбери пункт меню ниже 👇", reply_markup=MAIN_MENU)
    return ConversationHandler.END


async def service_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    mapping = {
        "service_turnkey": "🤖 Бот под ключ — меню, логика, база, админка, уведомления.",
        "service_shop": "🛍 Бот-магазин — каталог, карточки товаров, корзина, заказ.",
        "service_leads": "📩 Бот заявок — сбор клиентов, анкеты, запись, уведомления.",
        "service_payment": "💳 Бот с оплатой — интеграция платёжных систем и автостатусы.",
    }

    text = mapping.get(query.data, "Услуга не найдена.")
    await query.message.reply_text(
        f"<b>Пример услуги</b>\n\n{text}\n\n"
        "Такой блок хорошо показывает клиенту, что именно ты умеешь делать.",
        parse_mode=ParseMode.HTML,
    )


async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    order = context.user_data.get("order", OrderDraft())
    order.name = (update.message.text or "").strip()
    context.user_data["order"] = order

    await update.message.reply_text(
        "Выберите тип бота для примера заказа:\n"
        "1. Бот под ключ\n"
        "2. Магазин\n"
        "3. Заявки\n"
        "4. Оплата\n\n"
        "Напишите вариант текстом."
    )
    return ASK_SERVICE


async def ask_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    order = context.user_data.get("order", OrderDraft())
    order.service = (update.message.text or "").strip()
    context.user_data["order"] = order

    await update.message.reply_text(
        "Кратко опишите, что нужно клиенту.\n"
        "Например: каталог товаров, кнопки, оплата, админка."
    )
    return ASK_DETAILS


async def ask_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    order = context.user_data.get("order", OrderDraft())
    order.details = (update.message.text or "").strip()
    context.user_data["order"] = order

    summary = (
        "<b>Заявка оформлена (демо)</b>\n\n"
        f"👤 Имя: {order.name}\n"
        f"🛠 Услуга: {order.service}\n"
        f"📝 Детали: {order.details}\n\n"
        "В реальном боте заявка может:\n"
        "• отправляться админу\n"
        "• сохраняться в Google Sheets / БД\n"
        "• уходить в CRM\n"
        "• запускать автоответ клиенту"
    )

    await update.message.reply_text(summary, parse_mode=ParseMode.HTML, reply_markup=MAIN_MENU)

    if ADMIN_ID:
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=(
                    "Новая заявка (демо):\n"
                    f"Имя: {order.name}\n"
                    f"Услуга: {order.service}\n"
                    f"Детали: {order.details}"
                ),
            )
        except Exception as exc:
            logger.warning("Failed to send admin notification: %s", exc)

    return ConversationHandler.END


async def support_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()

    await update.message.reply_text(
        "<b>Сообщение в поддержку отправлено (демо)</b>\n\n"
        f"Текст: {text}\n\n"
        "В рабочей версии можно пересылать это сообщение админу или подключать оператора.",
        parse_mode=ParseMode.HTML,
        reply_markup=MAIN_MENU,
    )

    if ADMIN_ID:
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"Обращение в поддержку (демо):\n{text}",
            )
        except Exception as exc:
            logger.warning("Failed to send support message to admin: %s", exc)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Действие отменено.", reply_markup=MAIN_MENU)
    return ConversationHandler.END


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("Set BOT_TOKEN environment variable before запуском.")

    app = Application.builder().token(BOT_TOKEN).build()

    conversation = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, menu_router)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            ASK_SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_service)],
            ASK_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_details)],
            SUPPORT_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, support_message)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_message=False,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(service_callback, pattern=r"^service_"))
    app.add_handler(conversation)

    logger.info("Bot started")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
