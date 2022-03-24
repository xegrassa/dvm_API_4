import os.path
from pathlib import Path
from urllib.parse import urlparse, unquote

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


def fetch_nasa():
    token = os.getenv('NASA_TOKEN')
    url = f'https://api.nasa.gov/planetary/apod?count=30&api_key={token}'
    response = requests.get(url)
    response.raise_for_status()
    links = [img_info['url'] for img_info in response.json() if img_info['media_type'] == 'image']
    for num, link in enumerate(links, start=1):
        ext = get_ext_from_url(link)
        download_image(link, f'images/nasa{num}{ext}')


def main():
    load_dotenv()
    Path("./images").mkdir(exist_ok=True)

    fetch_spacex_last_launch()
    fetch_nasa()


if __name__ == '__main__':
    main()
