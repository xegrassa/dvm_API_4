import os.path
from pathlib import Path
from urllib.parse import urlparse, unquote
from datetime import datetime
import requests
from dotenv import load_dotenv


def get_ext_from_url(url: str) -> str:
    """Возвращает расширение файла из url.

    ex: http://e1.ru/img/city.jpg -> .jpg
    """
    path = urlparse(unquote(url)).path
    ext = os.path.splitext(path)[1]
    return ext


def download_image(url, path):
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as f:
        f.write(response.content)


def fetch_spacex_last_launch():
    url = 'https://api.spacexdata.com/v3/launches/13'

    response = requests.get(url)
    response.raise_for_status()
    links = response.json()['links']['flickr_images']
    for num, link in enumerate(links, start=1):
        ext = get_ext_from_url(link)
        download_image(link, f'images/spacex{num}{ext}')


def fetch_nasa_apod():
    """Скачивает ~30 изображений дня."""
    token = os.getenv('NASA_TOKEN')
    url = f'https://api.nasa.gov/planetary/apod?count=30&api_key={token}'
    response = requests.get(url)
    response.raise_for_status()
    links = [img_info['url'] for img_info in response.json() if img_info['media_type'] == 'image']
    for num, link in enumerate(links, start=1):
        ext = get_ext_from_url(link)
        download_image(link, f'images/nasa{num}{ext}')


def fetch_nasa_epic():
    token = os.getenv('NASA_TOKEN')
    url = f'https://api.nasa.gov/EPIC/api/natural/images?api_key={token}'
    response = requests.get(url)
    response.raise_for_status()
    images_info = [(image['image'], datetime.fromisoformat(image['date'])) for image in response.json()]

    for num, image_info in enumerate(images_info[:10], start=1):
        name, date = image_info
        year, month, day = date.year, date.month, date.day
        link = f'https://api.nasa.gov/EPIC/archive/natural/{year}/{month:0=2}/{day:0=2}/png/{name}.png?api_key={token}'
        download_image(link, f'images/nasa_epic{num}.png')


def main():
    load_dotenv()
    Path("./images").mkdir(exist_ok=True)

    # fetch_spacex_last_launch()
    # fetch_nasa_apod()
    fetch_nasa_epic()


if __name__ == '__main__':
    main()
