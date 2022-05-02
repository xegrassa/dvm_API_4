from pathlib import Path

import requests

from core.constant import LOGGER_NAME
from core.helpers import configure_logger, download_image, get_ext_from_url


def fetch_spacex_last_launch():
    """Скачивает изображения запуска кораблей с SpaceX."""
    url = 'https://api.spacexdata.com/v3/launches/13'

    response = requests.get(url)
    response.raise_for_status()
    links = response.json()['links']['flickr_images']
    for num, link in enumerate(links, start=1):
        ext = get_ext_from_url(link)
        download_image(link, f'images/spacex{num}{ext}')


if __name__ == '__main__':
    configure_logger(LOGGER_NAME, 2)
    Path("./images").mkdir(exist_ok=True)
    fetch_spacex_last_launch()
