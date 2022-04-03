import argparse
import logging
import os.path
import time
from pathlib import Path

import telegram
from dotenv import load_dotenv
from telegram import InputMediaPhoto
from telegram.error import RetryAfter, BadRequest

from fetch_nasa import fetch_nasa_apod, fetch_nasa_epic
from fetch_spacex import fetch_spacex_last_launch
from helpers import get_image_paths, get_part_media

logger = logging.getLogger('API4')


def send_images_to_telegram(chat_id: str, image_paths: list[str]):
    """Отправляет в телеграмм канал посты с изображениями."""
    media = []
    for path in image_paths:
        image = InputMediaPhoto(media=open(path, 'rb'))
        if len(image.media.input_file_content) < 11 ** 6:
            media.append(image)

    token = os.getenv('TELEGRAM_TOKEN')
    bot = telegram.Bot(token=token)

    for part in get_part_media(media, 8):
        try:
            bot.send_media_group(chat_id=f'@{chat_id}', timeout=40, media=part)
        except RetryAfter as e:
            timeout = e.retry_after + 1
            logger.info(f'Ждем флуд таймаут {timeout}')
            time.sleep(timeout)
            bot.send_media_group(chat_id=f'@{chat_id}', timeout=40, media=part)
        except BadRequest:
            logger.debug(f'Был BadRequest для набора изображений. '
                         f'Не будут отправлены {[image.media.filename for image in part]}.')
        time.sleep(5)


def _configure_loggers(verbose):
    if verbose > 1:
        logging_level = logging.DEBUG
    elif verbose == 1:
        logging_level = logging.INFO
    else:
        logging_level = logging.NOTSET

    ch = logging.StreamHandler()
    ch.setLevel(logging_level)
    formatter = logging.Formatter(f'%(asctime)s:%(levelname)s:%(module)s:%(message)s')
    ch.setFormatter(formatter)

    logger.setLevel(logging_level)
    logger.addHandler(ch)


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description='Скачивает и отправляет изображения связанные с космосом в телеграмм канал')
    parser.add_argument('chat_id', help='ID канала в телеграм куда бот отправит фотографии. Например "dvmn_flood"')
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
