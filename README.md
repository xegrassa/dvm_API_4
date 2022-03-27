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
NASA_TOKEN = Ваш_токен_от_NASA
```

## Получение NASA_TOKEN
- Получить токен можно заполнив форму на сайте [api.nasa.gov](https://api.nasa.gov/). 
- После ТОКЕН придет на указанный email

![img](https://user-images.githubusercontent.com/52129535/160269361-a66b2c4a-79f8-431a-b275-bc330e1111da.jpg)

## Запуск

Находясь в корне проекта запустите проект командой
```
python main.py
```

После запуска в корне проекта создастся директория **images** в которую будут скачаны фотографии

## Зависимости

* [Python 3.10](https://www.python.org/)
* [Requests](https://docs.python-requests.org/en/latest/)
* [python-dotenv](https://github.com/theskumar/python-dotenv)