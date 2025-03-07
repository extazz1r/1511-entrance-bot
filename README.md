🤖 Telegram GPT Бот

Этот проект представляет собой Telegram-бота, который использует OpenAI GPT для обработки и генерации ответов на основе данных из файла. Бот работает с aiogram и асинхронным API OpenAI.

📌 Функционал

Обрабатывает сообщения пользователей в Telegram.

Использует aiogram для управления ботом.

Загружает контекстные данные из data.txt и использует их для генерации ответов.

Подключается к OpenAI GPT через асинхронный клиент.

Поддерживает работу через прокси (если требуется).

Логирует все действия, включая запросы и ответы.

🚀 Установка и запуск

🔹 1. Клонирование репозитория

git clone https://github.com/your-repo/telegram-gpt-bot.git
cd telegram-gpt-bot

🔹 2. Создание виртуального окружения и установка зависимостей

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

🔹 3. Настройка .env (переменные окружения)

Создайте файл .env и добавьте в него:

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key

🔹 4. Запуск бота

python bot.py

⚙️ Как работает код?

📌 Основные компоненты:

Инициализация бота:

Загружается токен Telegram-бота из .env.

Создается объект Bot с aiogram.

Настраивается Dispatcher.

Чтение контекста из файла:

Бот загружает текст из data.txt и использует его как контекст для OpenAI.

Если файл отсутствует, бот сообщает об этом в логах.

Обработка сообщений:

При старте (/start) бот отправляет приветственное сообщение.

Любой текст пользователя отправляется в OpenAI.

Ответ редактируется в сообщении "Ваш запрос обрабатывается...".

Запрос к OpenAI:

GPT получает сообщение пользователя + загруженный контекст.

Бот отправляет запрос в OpenAI.

Полученный ответ отправляется пользователю.

Логирование:

Все запросы и ответы записываются в логи (используется rich.logging).

В логах отображаются username и ID пользователя.

🔧 Развертывание на сервере

📌 Автозапуск через systemd

Создайте файл сервиса:

sudo nano /etc/systemd/system/bot.service

Добавьте:

[Unit]
Description=Telegram GPT Bot
After=network.target

[Service]
User=user
WorkingDirectory=/home/user/bot
ExecStart=/home/user/bot/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target

Сохраните (CTRL+X, Y, ENTER) и запустите:

sudo systemctl daemon-reload
sudo systemctl enable bot
sudo systemctl start bot

Проверка логов:

journalctl -u bot -f

📜 Лицензия

Проект распространяется под лицензией GNU General Public License v3.0.

