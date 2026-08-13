# Ame v0.0.1

Первый рабочий прототип цифрового компаньона Аме в Telegram.

Пользователь пишет текст боту, бот отправляет `personality/ame.md` как системную инструкцию вместе с сообщением в OpenAI Responses API (`gpt-5.4-mini`) и возвращает ответ в характере Аме.

## Что входит

- Python 3.10+;
- aiogram 3 и long polling Telegram;
- OpenAI Responses API;
- `personality/ame.md` как системный промпт;
- понятные ответы при временных ошибках API;
- Docker Compose для постоянного запуска на сервере.

В v0.0.1 намеренно нет истории и долговременной памяти, голоса, аватара, инициативных сообщений, доступа к экрану и управления компьютером. Каждый запрос к модели независим.

## Настройка ключей

1. Скопируйте `.env.example` в `.env`.
2. Откройте `.env` и вставьте:

```env
TELEGRAM_BOT_TOKEN=токен_из_BotFather
OPENAI_API_KEY=ключ_OpenAI_API
LLM_MODEL=gpt-5.4-mini
```

Файл `.env` исключён из Git. Не добавляйте реальные ключи в `.env.example`, README, коммиты или сообщения об ошибках.

## Локальный запуск

PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

После строки о запуске polling откройте бота в Telegram, отправьте `/start`, а затем обычное текстовое сообщение, например `аме ты живая`.

Остановить бота: `Ctrl+C`.

## Запуск через Docker Compose

После заполнения `.env`:

```bash
docker compose up -d --build
docker compose logs -f ame
```

Обновление:

```bash
git pull --ff-only
docker compose up -d --build
```

## Структура

```text
.
├── app/
│   ├── bot.py
│   ├── config.py
│   └── llm.py
├── personality/
│   └── ame.md
├── .env.example
├── compose.yaml
├── Dockerfile
├── main.py
└── requirements.txt
```

## Быстрая диагностика

- Ошибка о переменных окружения: проверьте `.env` и названия `TELEGRAM_BOT_TOKEN`, `OPENAI_API_KEY`.
- Telegram сообщает `Unauthorized`: токен BotFather неверный или отозван.
- Ошибка модели/лимита: проверьте доступ API-проекта к `gpt-5.4-mini`, баланс и лимиты OpenAI.
- `Conflict: terminated by other getUpdates request`: тот же Telegram-токен уже запущен во втором экземпляре; оставьте только один polling-процесс.
