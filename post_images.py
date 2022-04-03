import argparse
import logging
import os.path
import time
from pathlib import Path

import telegram
from dotenv import load_dotenv
from telegram import InputMediaPhoto

from fetch_nasa import fetch_nasa_apod, fetch_nasa_epic
from fetch_spacex import fetch_spacex_last_launch
from helpers import get_image_paths

logger = logging.getLogger('API4')


def send_images_to_telegram(image_paths: list[str]):
    """Отправляет в телеграмм канал пост с изображениями."""
    media = []
    for path in image_paths:
        media.append(InputMediaPhoto(media=open(path, 'rb')))

    token = os.getenv('TELEGRAM_TOKEN')
    bot = telegram.Bot(token=token)
    bot.send_media_group(chat_id=TELEGRAM_CHAT_ID, media=media)


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description='Скачивает и отправляет изображения связанные с космосом в телеграмм канал')
    parser.add_argument('--delay', type=int, default=int(os.getenv('POST_IMAGE_DELAY', default=86400)),
                        help='Задержка отправки изображений в сек.(По умолчанию берется из окружения и равна 1 дню)')
    parser.add_argument('--verbose', '-v', action='count', default=0,
                        help='Выводит больше информации. Максимум 2 уровня')
    args = parser.parse_args()

    _configure_loggers(args.verbose)

    Path("./images").mkdir(exist_ok=True)
    while True:
        fetch_spacex_last_launch()
        fetch_nasa_apod()
        fetch_nasa_epic()

        image_paths = get_image_paths()
        logger.info(f'Изображения скачаны: {len(image_paths)}')

        send_images_to_telegram(args.chat_id, image_paths)
        for path in image_paths:
            os.remove(path)

        logger.info(f'Отправка изображений завершена. Следующая отправка через {args.delay}')
        time.sleep(args.delay)


if __name__ == '__main__':
    main()
