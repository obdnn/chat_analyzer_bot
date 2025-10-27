from aiogram import Router, F
from aiogram.types import Message
from bot.utils.sentiment import analyze_sentiment
from bot.database.db import save_message
import os
from dotenv import load_dotenv, find_dotenv
from google import genai

load_dotenv(find_dotenv())
router = Router()

client = genai.Client(api_key=os.getenv('API_AI'))

@router.message(F.text & ~F.text.startswith("/"))
async def analyze_message(message: Message):
    chat_id = str(message.chat.id)
    text = message.text
    user = message.from_user.username or str(message.from_user.id)
    chat_type = message.chat.type

    color = await analyze_sentiment(client, text)
    await save_message(text=text, user=user, color=color, chat_id=chat_id)

    if chat_type == "private":
        await message.answer(f"✅ Сообщение сохранено. Тональность: {color}")
    else:
        print(f"[{chat_type}] {user}: {color}")
