import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
import httpx
from aiogram.client.default import DefaultBotProperties
from openai import AsyncOpenAI
from rich.logging import RichHandler

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[RichHandler()]  # Красивый вывод логов
)
logger = logging.getLogger(__name__)

# Токены
TELEGRAM_BOT_TOKEN = "ТУТ ТОКЕН БОТА"
OPENAI_API_KEY = "ТОКЕН ОПЕН АИ"

# Прокси
PROXY_URL = "ТУТ УРЛ ПРОКСИ"
PROXY_AUTH = "ТУТ АВТОРИЗАЦИЯ ПРОКСИ"

# Инициализация бота и диспетчера
bot = Bot(
    token=TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)
dp = Dispatcher()

# Настройка клиента OpenAI с прокси
client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.openai.com/v1",
    http_client=httpx.AsyncClient(
        proxies=f"http://{PROXY_AUTH}@{PROXY_URL.split('//')[1]}",
        transport=httpx.HTTPTransport(local_address="0.0.0.0")
    )
)

# Асинхронное чтение файла
async def load_data_from_file():
    try:
        logger.info("Загрузка данных из файла data.txt...")
        return await asyncio.to_thread(lambda: open("data.txt", "r", encoding="utf-8").read())
    except Exception as e:
        logger.error(f"Ошибка чтения файла: {e}")
        return "Контекст не найден."

# Асинхронный запрос в OpenAI
async def ask_gpt(user_message: str):
    logger.info(f"Запрос к GPT: {user_message}")
    context_data = await load_data_from_file()
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Используй только эти данные как контекст: {context_data}. "
                                                 "Не добавляй информацию, которая не содержится в этих данных."},
                {"role": "user", "content": user_message}
            ]
        )
        result = response.choices[0].message.content
        logger.info(f"Ответ GPT: {result}")
        return result
    except Exception as e:
        logger.error(f"Ошибка при запросе к OpenAI: {e}")
        return "Произошла ошибка при обработке запроса."

# Обработчик команды /start
@dp.message(Command("start"))
async def start(message: Message):
    username = message.from_user.username or message.from_user.full_name
    logger.info(f"Пользователь {username} ({message.from_user.id}) запустил бота.")
    await message.answer("Привет! Я ваш консультант по лицею 1511. Задавайте вопросы!")

# Обработчик сообщений
@dp.message()
async def chat_with_gpt(message: Message):
    user_text = message.text
    username = message.from_user.username or message.from_user.full_name
    logger.info(f"Получено сообщение от {username} ({message.from_user.id}): {user_text}")

    processing_message = await message.answer("Ваш запрос обрабатывается...")
    response = await ask_gpt(user_text)
    await processing_message.edit_text(f"Ответ: {response}")

# Запуск бота
async def main():
    logger.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
