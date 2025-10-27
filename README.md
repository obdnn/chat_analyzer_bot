# 🤖 Chat Analyzer Bot

Chat Analyzer Bot — a Telegram bot built with **Aiogram 3** and **SQLAlchemy**, designed to analyze chat messages, detect sentiment (positive, negative, neutral), and generate statistics for both chats and individual users.

---

## 🌟 Features
- 📩 Collects and stores chat messages in a PostgreSQL database  
- 🧠 Performs **sentiment analysis** using Google GenAI API  
- 📊 Generates statistics per chat or per user  
- ⚡ Asynchronous architecture with **AsyncPG**  
- 🗄️ ORM via **SQLAlchemy**  
- 🔐 Uses `.env` file for secure API key and DB credentials storage  

---

## 🧰 Tech Stack
| Technology | Purpose |
|-------------|----------|
| **Python 3.11+** | Core language |
| **Aiogram 3.22.0** | Telegram Bot framework |
| **SQLAlchemy 2.0** | ORM for PostgreSQL |
| **AsyncPG** | Async database driver |
| **Google GenAI API** | Sentiment analysis |
| **python-dotenv** | Environment configuration |

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/obdnnn/chat_analyzer_bot.git
cd chat_analyzer_bot
```

2️⃣ Create and activate a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate   # Linux/Mac
```
3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
4️⃣ Create a .env file and add your credentials
```bash
BOT_TOKEN=your_telegram_bot_token
API_AI=your_google_genai_api_key
```
5️⃣ Initialize the database
```bash
python -m bot.database.db
```
6️⃣ Run the bot
```bash
python main.py
```