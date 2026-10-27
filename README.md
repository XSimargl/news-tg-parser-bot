# News parsing bot

Telegram-бот для сбора новостей из RSS-лент, отбора и суммаризации материалов с помощью Google Gemini и отправки результатов в Telegram.

## Требования

- Python 3.10 или новее
- Токен Telegram-бота от [@BotFather](https://t.me/BotFather)
- API-ключ Google Gemini из [Google AI Studio](https://aistudio.google.com/apikey)
- Числовой ID чата Telegram, в который бот будет отправлять новости

## Установка

Создайте и активируйте виртуальное окружение, затем установите зависимости:

```shell
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```shell
source .venv/bin/activate
```

Установка пакетов:

```shell
python -m pip install -r requirements.txt
```

## Настройка

Создайте в корне проекта файл `.env` и укажите в нём:

```dotenv
API_KEY_TG=токен_telegram_бота
ADMIN_CHAT_ID=числовой_id_чата
API_GEMINI=ключ_google_gemini
```

## Запуск

Из корневой папки проекта выполните:

```shell
python main.py
```

Бот создаёт SQLite-базу в `database/news.db`, проверяет RSS-ленты, обрабатывает новости и отправляет одобренные материалы в Telegram. После обработки очередного цикла бот ждёт один час до следующей проверки. Для остановки нажмите `Ctrl+C`.
