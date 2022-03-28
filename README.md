# Скачиватель фотографий космоса

Приложение скачивает фотографии космоса с сайтов [SpaceX](https://www.spacex.com/) и [NASA](https://www.nasa.gov/). (**Проект учебный**)

## Установка

Клонируйте проект и установите зависимости командами ниже.

```
git clone https://github.com/xegrassa/dvm_API_4.git
cd dvm_API_4
pip install -r requirements.txt
```

Для работы в корне проекта создайте файл **.env**
```
NASA_TOKEN=Ваш_токен_от_NASA
TELEGRAM_TOKEN=Ваш_токен_от_Telegram_бота
POST_IMAGE_DELAY=86400
```

## Получение NASA_TOKEN
- Получить токен можно заполнив форму на сайте [api.nasa.gov](https://api.nasa.gov/). 
- После ТОКЕН придет на указанный email

## Получение TELEGRAM_TOKEN
- [Как получить token](https://way23.ru/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B1%D0%BE%D1%82%D0%B0-%D0%B2-telegram.html)

## Запуск
Мини справку о работе можно вызвать через опцию -h. `python main.py -h`

Можно поменять периодичность отправки изображений через переменную окружения `POST_IMAGE_DELAY` или добавив параметр при запуске `--delay КОЛ-ВО_СЕК`

Находясь в корне проекта запустите проект командой
```
python main.py
```

После запуска в корне проекта создастся директория **images** в которую будут скачаны фотографии

## Зависимости

* [Python 3.10](https://www.python.org/)
* [Requests](https://docs.python-requests.org/en/latest/)
* [python-dotenv](https://github.com/theskumar/python-dotenv)
* [python-telegram-bot](https://python-telegram-bot.org/)