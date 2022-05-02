import argparse
import logging
import os.path
import time
from pathlib import Path

from dotenv import load_dotenv
from telegram import InputMediaPhoto

from core.constant import LOGGER_NAME, PART_OF_IMAGES_COUNT, POST_IMAGE_DELAY
from core.helpers import configure_logger, filter_images_by_size, get_image_paths, send_images_to_telegram
from fetch_nasa import fetch_nasa_apod, fetch_nasa_epic
from fetch_spacex import fetch_spacex_last_launch

logger = logging.getLogger(LOGGER_NAME)


def main():
    Path("./images").mkdir(exist_ok=True)

    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    nasa_token = os.getenv('NASA_TOKEN')

    parser = argparse.ArgumentParser(
        description='Скачивает и отправляет изображения связанные с космосом в телеграмм канал')
    parser.add_argument('chat_id', help='ID канала в телеграм куда бот отправит фотографии. Например "dvmn_flood"')
    parser.add_argument('--delay', type=int, default=int(os.getenv('POST_IMAGE_DELAY', default=POST_IMAGE_DELAY)),
                        help='Задержка отправки изображений в сек.(По умолчанию берется из окружения и равна 1 дню)')
    parser.add_argument('--verbose', '-v', action='count', default=0,
                        help='Выводит больше информации. -v, -vv')
    args = parser.parse_args()

    configure_logger(LOGGER_NAME, args.verbose)

    while True:
        fetch_spacex_last_launch()
        fetch_nasa_apod(nasa_token)
        fetch_nasa_epic(nasa_token)

        image_paths = filter_images_by_size(get_image_paths())
        logger.info(f'Загружено изображений: {len(image_paths)}')

        images = []
        for path in image_paths:
            with open(path, 'rb') as f:
                images.append(InputMediaPhoto(media=f))

        for start_index in range(len(images), PART_OF_IMAGES_COUNT):
            images_part = images[start_index:start_index + PART_OF_IMAGES_COUNT]
            send_images_to_telegram(telegram_token, args.chat_id, images_part)

        for path in image_paths:
            os.remove(path)

        logger.info(f'Отправка изображений завершена. Следующая отправка через {args.delay}')
        time.sleep(args.delay)


if __name__ == '__main__':
    main()
