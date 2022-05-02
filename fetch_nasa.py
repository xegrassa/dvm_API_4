import logging
import os
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

from core.constant import LOGGER_NAME, NASA_APOD_COUNT, NASA_EPIC_COUNT
from core.helpers import configure_logger, download_image, get_ext_from_url

logger = logging.getLogger(LOGGER_NAME)

def fetch_nasa_apod(token):
    """Скачивает изображения дня с NASA APOD."""
    payload = {
        'api_key': token,
        'count': NASA_APOD_COUNT,
    }
    url = f'https://api.nasa.gov/planetary/apod'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    links = [img_info['url'] for img_info in response.json() if img_info['media_type'] == 'image']
    for num, link in enumerate(links, start=1):
        ext = get_ext_from_url(link)
        download_image(link, f'images/nasa{num}{ext}')


def fetch_nasa_epic(token):
    """Скачивает изображения космоса с NASA.EPIC."""
    payload = {'api_key': token}
    url = f'https://api.nasa.gov/EPIC/api/natural/images'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    images_info = [(image['image'], datetime.fromisoformat(image['date'])) for image in response.json()]

    for num, image_info in enumerate(images_info[:NASA_EPIC_COUNT], start=1):
        name, date = image_info
        year, month, day = date.year, date.month, date.day
        link = f'https://api.nasa.gov/EPIC/archive/natural/{year}/{month:0=2}/{day:0=2}/png/{name}.png'
        query = f'?{urlencode(payload)}'
        download_image(link + query, f'images/nasa_epic{num}.png')


if __name__ == '__main__':
    configure_logger(LOGGER_NAME, 2)
    load_dotenv()
    nasa_token = os.getenv('NASA_TOKEN')

    Path("./images").mkdir(exist_ok=True)
    fetch_nasa_apod(nasa_token)
    fetch_nasa_epic(nasa_token)
