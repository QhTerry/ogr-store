"""
OGR Store — бот-лаунчер для Mini App.
Его задача — открыть витрину внутри Telegram. Всё остальное живёт в index.html.

Запуск:
  pip install aiogram>=3.7 python-dotenv
  заполнить .env (BOT_TOKEN + WEBAPP_URL)
  python launcher_bot.py
"""
import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton,
    WebAppInfo, MenuButtonWebApp,
)
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger("ogr-launcher")

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
WEBAPP_URL = os.getenv("WEBAPP_URL", "")          # https-адрес, где лежит index.html
MANAGER_CHAT_ID = int(os.getenv("MANAGER_CHAT_ID", "0"))

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


def shop_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🛍 Открыть магазин", web_app=WebAppInfo(url=WEBAPP_URL)),
    ]])


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 <b>Добро пожаловать в OGR Store</b>\n\n"
        "Оригинальная техника Apple, Samsung и консоли — с гарантией и доставкой по РФ.\n\n"
        "Нажмите кнопку ниже, чтобы открыть витрину 👇\n\n"
        "🛡 Единственный официальный бот — @OgrStoreBot, канал — @ogrstore.",
        reply_markup=shop_kb(),
    )


@dp.message(lambda m: m.web_app_data is not None)
async def on_webapp_data(message: Message):
    """
    Если позже включим отправку заказа из Mini App (sendData) —
    данные прилетят сюда, и мы перешлём их менеджеру.
    Сейчас checkout визуальный, так что это задел на будущее.
    """
    data = message.web_app_data.data
    note = f"🆕 <b>Заказ из Mini App</b>\n\n{data}"
    target = MANAGER_CHAT_ID or message.from_user.id
    await bot.send_message(target, note)
    await message.answer("✅ Заявка получена, менеджер свяжется с вами!")


async def main():
    if not BOT_TOKEN or not WEBAPP_URL:
        log.error("Заполните .env: нужны BOT_TOKEN и WEBAPP_URL (https-адрес index.html)")
        sys.exit(1)
    # синяя кнопка-меню слева от поля ввода — тоже открывает магазин
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="Магазин", web_app=WebAppInfo(url=WEBAPP_URL))
    )
    log.info("Лаунчер запущен ✅  WebApp: %s", WEBAPP_URL)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.info("Остановлен")
