from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import requests
from auth import *
from datetime import datetime
import wikipedia


vk_group_session = VkApi(token=TOKEN_GROUP)
longpoll = VkBotLongPoll(vk_group_session, '193813979')


def main():
    vk_g = vk_group_session.get_api()
    status = 0
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if status == 0:
                vk_g.messages.send(user_id=event.obj.message['from_id'],
                                 message="Напишите боту дату в формате YYYY-MM-DD, и он отправит в ответ день недели",
                                 random_id=random.randint(0, 2 ** 64))
                status = 1
            elif status == 1:
                vk_g.messages.send(user_id=event.obj.message['from_id'],
                                   message=datetime(*list(map(int, event.obj.message['text'].split('-')))).isoweekday(),
                                   random_id=random.randint(0, 2 ** 64))

if __name__ == '__main__':
    main()