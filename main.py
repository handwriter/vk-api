from vk_api import VkApi, VkUpload
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import requests
from auth import *
from datetime import datetime
import wikipedia
import sys
from io import BytesIO
import requests
from PIL import Image


vk_group_session = VkApi(token=TOKEN_GROUP)
vk_session = VkApi(token=TOKEN)
longpoll = VkBotLongPoll(vk_group_session, '193813979')


def main():
    vk_g = vk_group_session.get_api()
    vk = vk_session.get_api()
    status = 0
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(label="Схема", color=VkKeyboardColor.PRIMARY)  # Зелёный цвет
    keyboard.add_line()  # Следующие кнопки будут под этой
    keyboard.add_button(label="Спутник", color=VkKeyboardColor.PRIMARY)  # Синий цвет
    keyboard.add_button(label="Гибрид", color=VkKeyboardColor.PRIMARY)  # Белый цвет
    name_map = {'Схема': 'map',
                'Спутник': 'sat',
                'Гибрид': 'sat,skl'}
    name = ''
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if status == 0:
                vk_g.messages.send(user_id=event.obj.message['from_id'],
                                 message="Введите назвавние местности, фото которой вы хотите получить",
                                 random_id=random.randint(0, 2 ** 64))
                status = 1
            elif status == 1:
                name = event.obj.message['text']
                vk_g.messages.send(user_id=event.obj.message['from_id'],
                                   message="Выберите тип карты",
                                   keyboard=keyboard.get_keyboard(),
                                   random_id=random.randint(0, 2 ** 64))
                status = 2
            elif status == 2:
                toponym_to_find = name

                geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

                geocoder_params = {
                    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                    "geocode": toponym_to_find,
                    "format": "json"}

                response = requests.get(geocoder_api_server, params=geocoder_params)

                if not response:
                    # обработка ошибочной ситуации
                    pass

                # Преобразуем ответ в json-объект
                json_response = response.json()
                # Получаем первый топоним из ответа геокодера.
                toponym = json_response["response"]["GeoObjectCollection"][
                    "featureMember"][0]["GeoObject"]
                # Координаты центра топонима:
                toponym_coodrinates = toponym["Point"]["pos"]
                # Долгота и широта:
                toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

                delta = "0.005"

                # Собираем параметры для запроса к StaticMapsAPI:
                map_params = {
                    "ll": ",".join([toponym_longitude, toponym_lattitude]),
                    "spn": ",".join([delta, delta]),
                    "l": name_map[event.obj.message['text']]
                }

                map_api_server = "http://static-maps.yandex.ru/1.x/"
                # ... и выполняем запрос
                response = requests.get(map_api_server, params=map_params)
                upload = VkUpload(vk_session)
                Image.open(BytesIO(
                    response.content)).save('untitled.png')
                photo = upload.photo(  # Подставьте свои данные
                    'untitled.png',
                    album_id=271691298,
                    group_id=193813979
                )
                vk_photo_url = 'photo-{}_{}'.format(
                    193813979, photo[0]['id']
                )
                vk_g.messages.send(user_id=event.obj.message['from_id'],
                                   message=f"Это {toponym_to_find}. Что вы еще хотите увидеть?",
                                   attachment=vk_photo_url,
                                   random_id=random.randint(0, 2 ** 64))
                # Создадим картинку
                # и тут же ее покажем встроенным просмотрщиком операционной системы
                status = 1

if __name__ == '__main__':
    main()