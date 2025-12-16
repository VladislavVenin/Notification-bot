import requests
from requests.exceptions import ReadTimeout, ConnectionError
import decouple
import telegram
from pprint import pprint


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
    while True:
        try:
            response = requests.get(url, headers=headers, timeout=60, params=payload)
            response_payload = response.json()
            pprint(response_payload)
            lesson_title = response_payload["new_attempts"][0]["lesson_title"]
            message = f'У вас проверили работу "{lesson_title}"'
            if response_payload["new_attempts"][0]["is_negative"] is True:
                message += "\n\nК сожалению в работе нашлись ошибки."
            else:
                message += "\n\nПреподавателю всё понравилось, можно приступать к следующему уроку!"
            bot.send_message(decouple.config('CHAT_ID'), message)
            payload["timestamp"] = response_payload["new_attempts"][0]["timestamp"]
        except (ReadTimeout, ConnectionError) as e:
            print(e)
            continue


if __name__ == '__main__':
    main()
