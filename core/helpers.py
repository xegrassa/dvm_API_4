import logging
import os
import time
from urllib.parse import unquote, urlparse

import requests
import telegram
from telegram import InputMediaPhoto
from telegram.error import BadRequest, RetryAfter

from core.constant import LOGGER_NAME, MAX_RETRY_COUNT, MAX_SIZE_PHOTO_IN_BYTES
from core.error import ImagePathsEmpty

logger = logging.getLogger(LOGGER_NAME)


def get_ext_from_url(url: str) -> str:
    """Возвращает расширение файла из url.

    ex: http://e1.ru/img/city.jpg -> .jpg
    """
    path = urlparse(unquote(url)).path
    ext = os.path.splitext(path)[1]
    return ext


def get_image_paths() -> list[str]:
    """Возвращает список путей до изображений."""
    paths = []
    for root, _, files in os.walk('../images'):
        for file in files:
            paths.append(os.path.join(root, file))
    if not paths:
        raise ImagePathsEmpty('Папка с изображениям пуста.')
    return paths


def download_image(url: str, path: str):
    """Скачивает файл.

    :param url: url до файла
    :param path: Путь куда сохранить скачанный файл
    """
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as f:
        f.write(response.content)
    logger.debug(f'Скачано и сохранено изображение: {os.path.abspath(path)}')


def send_images_to_telegram(token: str, chat_id: str, images: list[InputMediaPhoto]):
    """Отправляет в телеграмм канал пост с изображениями.

    :param token: Токен для Телеграмм бота. Как получить https://core.telegram.org/bots#6-botfather
    :param chat_id: ID телеграм канала
    :param images: Изображения для отправки
    """
    bot = telegram.Bot(token=token)
    retry_count = MAX_RETRY_COUNT
    while retry_count >= 0:
        try:
            bot.send_media_group(chat_id=f'@{chat_id}', timeout=40, media=images)
            logger.debug(f'Успешно отправлены {[image.media.filename for image in images]}.')
            return
        except RetryAfter as e:
            timeout = e.retry_after + 1
            logger.info(f'Ждем флуд таймаут {timeout}')
            time.sleep(timeout)
        except BadRequest:
            time.sleep(2)
        retry_count -= 1
    logger.debug(f'Попытка отправки для набора изображений кончились. '
                 f'Не будут отправлены {[image.media.filename for image in images]}.')


def filter_images_by_size(image_paths: list[str]) -> list[str]:
    """Фильтрация изображений по размеру."""
    return [path for path in image_paths if os.stat(path).st_size < MAX_SIZE_PHOTO_IN_BYTES]


def configure_logger(logger_name: str, verbose: int = 0):
    """Настройка логгера."""
    logger_ = logging.getLogger(logger_name)
    if verbose > 1:
        logging_level = logging.DEBUG
    elif verbose == 1:
        logging_level = logging.INFO
    else:
        logging_level = logging.NOTSET

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level)
    formatter = logging.Formatter(f'%(asctime)s:%(levelname)s:%(module)s:%(message)s')
    console_handler.setFormatter(formatter)

    logger_.setLevel(logging_level)
    logger_.addHandler(console_handler)