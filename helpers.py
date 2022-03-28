from urllib.parse import urlparse, unquote
import os
import requests


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


def get_image_paths() -> list[str]:
    """Возвращает список путей до изображений."""
    paths = []
    for root, _, files in os.walk('images'):
        for file in files:
            paths.append(os.path.join(root, file))
    return paths
