from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import requests
from auth import *
from datetime import datetime
import wikipedia


vk_session = VkApi(token=TOKEN)
vk_group_session = VkApi(token=TOKEN_GROUP)
longpoll = VkBotLongPoll(vk_group_session, '193813979')


def main():
    vk = vk_session.get_api()
    vk_g = vk_group_session.get_api()
    attachments = [f'photo-{193813979}_{i["id"]}' for i in vk.photos.get(owner_id=-193813979, album_id='271691298')['items']]
    print(random.choice(attachments))
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk_g.messages.send(user_id=event.obj.message['from_id'],
                             message="Ответ",
                             attachment=random.choice(attachments),
                             random_id=random.randint(0, 2 ** 64))

if __name__ == '__main__':
    main()