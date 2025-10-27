from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from bot.database.db import SessionLocal, Message as MessageModel
from sqlalchemy import select, func

router = Router()


# 🚀 Команда /start
@router.message(CommandStart())
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Статистика по чату", callback_data="chat_stats")],
            [InlineKeyboardButton(text="👤 Статистика по пользователю", callback_data="choose_user")]
        ]
    )
    await message.answer("Выбери, что хочешь посмотреть:", reply_markup=keyboard)


# 📊 Статистика по чату
@router.callback_query(F.data == "chat_stats")
async def chat_stats(callback: CallbackQuery):
    chat_id = str(callback.message.chat.id)  # 👈 приводим к строке
    print(f"⚡ Получена статистика по чату {chat_id}")

    async with SessionLocal() as session:
        query = await session.execute(
            select(MessageModel.color, func.count(MessageModel.color))
            .where(MessageModel.chat_id == chat_id)
            .group_by(MessageModel.color)
        )
        stats = dict(query.all())

    if not stats:
        await callback.message.answer("Пока нет данных 📉")
        await callback.answer()
        return

    total = sum(stats.values())
    red = stats.get("красный", 0)
    green = stats.get("зеленый", 0)
    yellow = stats.get("желтый", 0)

    mood_index = (green * 1 + yellow * 0.5) / total * 100
    if mood_index < 30:
        mood = "😡 Настроение в чате — напряжённое!"
    elif mood_index < 60:
        mood = "😐 Настроение в чате — нейтральное."
    else:
        mood = "🌞 Настроение в чате — позитивное!"

    result = (
        f"📊 *Статистика по чату*\n\n"
        f"🟩 Позитивные: {round((green / total) * 100, 1)}% ({green})\n"
        f"🟨 Нейтральные: {round((yellow / total) * 100, 1)}% ({yellow})\n"
        f"🟥 Негативные: {round((red / total) * 100, 1)}% ({red})\n\n"
        f"🌡 *Температура чата:* {round(mood_index, 1)} / 100\n"
        f"{mood}\n"
        f"Всего сообщений: {total}"
    )

    await callback.message.answer(result, parse_mode="Markdown")
    await callback.answer()


# 👥 Выбор пользователя
@router.callback_query(F.data == "choose_user")
async def choose_user(callback: CallbackQuery):
    chat_id = str(callback.message.chat.id)  # 👈 тоже строка

    async with SessionLocal() as session:
        query = await session.execute(
            select(MessageModel.user).distinct().where(MessageModel.chat_id == chat_id)
        )
        users = [row[0] for row in query.fetchall()]

    if not users:
        await callback.message.answer("Нет данных о пользователях 📭")
        await callback.answer()
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"@{user}", callback_data=f"user_{user}")]
            for user in users
        ]
    )

    await callback.message.answer("Выбери пользователя:", reply_markup=keyboard)
    await callback.answer()


# 👤 Статистика по пользователю
@router.callback_query(F.data.startswith("user_"))
async def user_stats(callback: CallbackQuery):
    chat_id = str(callback.message.chat.id)  # 👈 приводим к строке
    target_user = callback.data.split("_", 1)[1]
    print(f"⚡ Получена статистика по пользователю {target_user} в чате {chat_id}")

    async with SessionLocal() as session:
        query = await session.execute(
            select(MessageModel.color, func.count(MessageModel.color))
            .where(MessageModel.user == target_user)
            .where(MessageModel.chat_id == chat_id)
            .group_by(MessageModel.color)
        )
        stats = dict(query.all())

    if not stats:
        await callback.message.answer(f"Для @{target_user} нет данных 📭")
        await callback.answer()
        return

    total = sum(stats.values())
    red = stats.get("красный", 0)
    green = stats.get("зеленый", 0)
    yellow = stats.get("желтый", 0)

    mood_index = (green * 1 + yellow * 0.5) / total * 100
    if mood_index < 30:
        mood = "😡 Преобладает негатив."
    elif mood_index < 60:
        mood = "😐 В основном нейтральные сообщения."
    else:
        mood = "🌞 Преобладает позитив."

    result = (
        f"👤 *Статистика для @{target_user}:*\n\n"
        f"🟩 Позитивные: {round((green / total) * 100, 1)}% ({green})\n"
        f"🟨 Нейтральные: {round((yellow / total) * 100, 1)}% ({yellow})\n"
        f"🟥 Негативные: {round((red / total) * 100, 1)}% ({red})\n\n"
        f"🌡 *Температура:* {round(mood_index, 1)} / 100\n"
        f"{mood}\n"
        f"Всего сообщений: {total}"
    )

    await callback.message.answer(result, parse_mode="Markdown")
    await callback.answer()
