from pathlib import Path

import requests

URL = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'


def main():
    Path("./images").mkdir(exist_ok=True)

    response = requests.get(URL)

    with open('images/hubble.jpeg', 'wb') as f:
        f.write(response.content)


if __name__ == '__main__':
    main()
