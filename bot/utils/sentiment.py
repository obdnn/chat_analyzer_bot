from google import genai
from google.genai.errors import APIError

SENTIMENT_PROMPT = """
Ты — эксперт по анализу тональности сообщений в чате.
Проанализируй сообщение и выбери один цвет, который отражает его эмоциональный тон:

- 'зеленый' — если сообщение выражает позитив, радость, благодарность, воодушевление или одобрение.
- 'желтый' — если сообщение нейтральное, описательное, содержит факт, вопрос или лёгкое недовольство без агрессии.
- 'красный' — если сообщение выражает раздражение, агрессию, обиду, сарказм, негативные эмоции или критику.

⚠️ Важно:
- Если сообщение звучит спокойно или констатирует факт, даже если в нём есть "не", выбирай 'желтый'.
- Если не уверен, выбирай 'желтый'.
- Не добавляй объяснений, только одно слово: 'красный', 'желтый' или 'зеленый'.
"""

async def analyze_sentiment(client: genai.Client, user_message: str) -> str:
    try:
        contents = [
            {"role": "user", "parts": [{"text": SENTIMENT_PROMPT}]},
            {"role": "user", "parts": [{"text": f"Сообщение: {user_message}"}]}
        ]

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents
        )
        return response.text.strip().lower()

    except APIError as e:
        return f"ошибка API: {e}"
    except Exception as e:
        return f"ошибка: {e}"


