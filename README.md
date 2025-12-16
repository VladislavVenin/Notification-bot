# Бот для получения уведомлений о проверке работ
Телеграм бот для получения уведомлений о проверке работ на курсе Devman

## Установка
Проект был написан на Python 3.10.9 

Скачайте код с GitHub. Затем установите зависимости
```
pip install -r requirements.txt
```
Создайте файл `.env` и определите следующие переменные окружения:
- `DEVMAN_TOKEN` - Ваш токен на сайте devman, получить его можно по [этой ссылке](https://dvmn.org/api/docs/)
- `TG_BOT` - Токен вашего телеграм бота, его можно узнать в [BotFather](https://telegram.me/BotFather)
- `CHAT_ID` - ID вашего чата, чтобы его получить напишите [специальному боту](https://telegram.me/userinfobot)

## Запуск
```
python main.py
```
После проверки вам придёт уведомление от бота:

<img width="491" height="209" alt="Telegram_2025-12-17_02-14-11" src="https://github.com/user-attachments/assets/390b95ab-b727-41c9-a0d1-cb02702d8b4f" />

