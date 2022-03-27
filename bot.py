import os

import telegram
from dotenv import load_dotenv


def main():
    token = os.getenv('TELEGRAM_TOKEN')
    bot = telegram.Bot(token=token)
    print(bot.get_me())
    bot.send_message(chat_id='@space_images_dvmn', text="Сообщение для проверки")
    bot.send_photo(chat_id='@space_images_dvmn', photo=open('images/nasa_epic1.png', 'rb'))


if __name__ == '__main__':
    load_dotenv()
    main()
