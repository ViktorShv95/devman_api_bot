import requests
import os
import telegram
from dotenv import load_dotenv


def main():

    load_dotenv()

    bot = telegram.Bot(token=os.getenv('BOT_TOKEN'))
    chat_id = os.getenv('CHAT_ID')

    while True:
        devman_api_url = 'https://dvmn.org/api/long_polling/'
        headers = {
            'Authorization': f"Token {os.environ['DEVMAN_TOKEN']}"
        }
        params = {}
        response = requests.get(devman_api_url, headers=headers, params=params)
        response.raise_for_status()
        response_data = response.json()
        if response_data['status'] == 'found':
            params['timestamp'] = response_data['last_attempt_timestamp']

            new_attempt = response_data['new_attempts'][0]
            is_negative = new_attempt['is_negative']
            lesson_title = new_attempt['lesson_title']
            lesson_url = f'https://dvmn.org{new_attempt["lesson_url"]}'

            if is_negative:
                bot.send_message(chat_id=chat_id,
                                 text=f'Работа "{lesson_title}" проверена.\n'
                                 f'К сожалению, в работе были найдены ошибки.\n{lesson_url}')
            else:
                bot.send_message(chat_id=chat_id,
                                 text=f'Работа "{lesson_title}" проверена.\nПреподавателю всё понравилось!'
                                 f' Можно приступать к следующему заданию!\n{lesson_url}')

        elif response_data['status'] == 'timeout':
            params['timestamp'] = response_data['timestamp_to_request']

if __name__ == '__main__':
    main()