from pprint import pprint
import logging
import time

import decouple
import telegram
import requests
from requests.exceptions import ReadTimeout, ConnectionError


class TelegramHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(self.chat_id, log_entry)


def main():
    bot_api_key = decouple.config('TG_BOT')
    bot = telegram.Bot(token=bot_api_key)
    chat_id = decouple.config('CHAT_ID')

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logging.basicConfig(
        format="%(asctime)s (%(process)d) %(levelname)s: %(message)s",
        datefmt='%d/%m/%Y %I:%M:%S'
    )
    tg_formatter = logging.Formatter("%(levelname)s: %(message)s")

    tg_handler = TelegramHandler(bot, chat_id)
    tg_handler.setFormatter(tg_formatter)
    logger.addHandler(tg_handler)

    devman_token = decouple.config('DEVMAN_TOKEN')
    headers = {
        'Authorization': devman_token
    }
    url = "https://dvmn.org/api/long_polling/"
    payload = {
        "timestamp": None
    }
    logging.info("Бот запущен...")
    while True:
        try:
            response = requests.get(url, headers=headers, timeout=90, params=payload)
            response.raise_for_status()
            response_payload = response.json()
            pprint(response_payload)
            lesson_title = response_payload["new_attempts"][0]["lesson_title"]
            message = f'У вас проверили работу "{lesson_title}"'
            if response_payload["new_attempts"][0]["is_negative"] is True:
                message += "\n\nК сожалению в работе нашлись ошибки."
            else:
                message += "\n\nПреподавателю всё понравилось, можно приступать к следующему уроку!"
            bot.send_message(chat_id, message)
            payload["timestamp"] = response_payload["new_attempts"][0]["timestamp"]
        except ReadTimeout:
            continue
        except KeyError as e:
            if response_payload["status"] != "timeout":
                logging.error(response_payload)
                logging.error(e)
            time.sleep(60)
            continue
        except ConnectionError as e:
            logging.error(e)
            half_an_hour = 1800
            time.sleep(half_an_hour)
            continue
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            time.sleep(60)


if __name__ == '__main__':
    main()
