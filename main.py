from pathlib import Path

import requests

URL = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
URL_2 = 'https://api.spacexdata.com/v3/launches/13'


def download_image(url, path):
    response = requests.get(URL)
    response.raise_for_status()
    with open(path, 'wb') as f:
        f.write(response.content)


def main():
    Path("./images").mkdir(exist_ok=True)

    download_image(URL, 'images/hubble.jpeg')

    response = requests.get(URL_2)
    response.raise_for_status()
    for link in response.json()['links']['flickr_images']:
        print(link)


if __name__ == '__main__':
    main()
