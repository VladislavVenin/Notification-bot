from pprint import pprint
from datetime import datetime
import time

import decouple
import telegram
import requests
from requests.exceptions import ReadTimeout, ConnectionError


def main():
    bot_api_key = decouple.config('TG_BOT')
    bot = telegram.Bot(token=bot_api_key)

    devman_token = decouple.config('DEVMAN_TOKEN')
    headers = {
        'Authorization': devman_token
    }
    url = "https://dvmn.org/api/long_polling/"
    payload = {
        "timestamp": None
    }
    print("Бот запущен...")
    while True:
        try:
            response = requests.get(url, headers=headers, timeout=90, params=payload)
            response.raise_for_status()
            response_payload = response.json()
            print(datetime.now())
            pprint(response_payload)
            lesson_title = response_payload["new_attempts"][0]["lesson_title"]
            message = f'У вас проверили работу "{lesson_title}"'
            if response_payload["new_attempts"][0]["is_negative"] is True:
                message += "\n\nК сожалению в работе нашлись ошибки."
            else:
                message += "\n\nПреподавателю всё понравилось, можно приступать к следующему уроку!"
            bot.send_message(decouple.config('CHAT_ID'), message)
            payload["timestamp"] = response_payload["new_attempts"][0]["timestamp"]
        except (ReadTimeout, KeyError):
            continue
        except ConnectionError as e:
            print(e)
            half_an_hour = 3600
            time.sleep(half_an_hour)
            continue


if __name__ == '__main__':
    main()
