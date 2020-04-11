from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import requests
from auth import TOKEN
from datetime import datetime
import wikipedia


vk_session = VkApi(token=TOKEN)


def main():
    vk = vk_session.get_api()
    print('\n'.join([i['sizes'][-1]['url'] for i in vk.photos.get(owner_id=-193813979, album_id='271691298')['items']]))


if __name__ == '__main__':
    main()