import requests

URL = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'


def main():
    response = requests.get(URL)

    with open('imgs/hubble.jpeg', 'wb') as f:
        f.write(response.content)


if __name__ == '__main__':
    main()
