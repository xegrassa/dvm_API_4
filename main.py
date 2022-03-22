from pathlib import Path

import requests


def fetch_spacex_last_launch():
    url = 'https://api.spacexdata.com/v3/launches/13'

    response = requests.get(url)
    response.raise_for_status()
    links = response.json()['links']['flickr_images']
    for num, link in enumerate(links, start=1):
        download_image(link, f'images/spacex{num}.jpg')


def download_image(url, path):
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as f:
        f.write(response.content)


def main():
    Path("./images").mkdir(exist_ok=True)

    fetch_spacex_last_launch()


if __name__ == '__main__':
    main()
