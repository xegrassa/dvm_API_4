LOGGER_NAME = 'API4'  # Имя логгера приложения

MAX_RETRY_COUNT = 2  # Кол-во попыток отправки изображений при ошибке
MAX_SIZE_PHOTO_IN_BYTES = 10_000_000  # В телеграмм нельзя отправить изображение больше этого размера
POST_IMAGE_DELAY = 86400  # Кол-во секунд в сутках, значение по умолчанию перед отправкой новых изображений

NASA_APOD_COUNT = 30  # Кол-во фотографий для скачивания с APOD
NASA_EPIC_COUNT = 10  # Кол-во фотографий для скачивания с EPIC

PART_OF_IMAGES_COUNT = 8  # Кол-во изображений отправляемых в 1 сообщении
