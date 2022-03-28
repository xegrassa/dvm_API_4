from datetime import datetime
import os
import requests

from helpers import get_ext_from_url, download_image

NASA_APOD_COUNT = 30
NASA_EPIC_COUNT = 10


def fetch_nasa_apod():
    """Скачивает изображения дня с NASA APOD."""
    token = os.getenv('NASA_TOKEN')
    url = f'https://api.nasa.gov/planetary/apod?count={NASA_APOD_COUNT}&api_key={token}'
    response = requests.get(url)
    response.raise_for_status()
    links = [img_info['url'] for img_info in response.json() if img_info['media_type'] == 'image']
    for num, link in enumerate(links, start=1):
        ext = get_ext_from_url(link)
        download_image(link, f'images/nasa{num}{ext}')


def fetch_nasa_epic():
    """Скачивает изображения космоса с NASA.EPIC."""
    token = os.getenv('NASA_TOKEN')
    url = f'https://api.nasa.gov/EPIC/api/natural/images?api_key={token}'
    response = requests.get(url)
    response.raise_for_status()
    images_info = [(image['image'], datetime.fromisoformat(image['date'])) for image in response.json()]

    for num, image_info in enumerate(images_info[:NASA_EPIC_COUNT], start=1):
        name, date = image_info
        year, month, day = date.year, date.month, date.day
        link = f'https://api.nasa.gov/EPIC/archive/natural/{year}/{month:0=2}/{day:0=2}/png/{name}.png?api_key={token}'
        download_image(link, f'images/nasa_epic{num}.png')


if __name__ == '__main__':
    fetch_nasa_apod()
    fetch_nasa_epic()
