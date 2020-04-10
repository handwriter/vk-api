from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import requests
from auth import TOKEN
from datetime import datetime
import wikipedia


vk_session = VkApi(token=TOKEN)
longpoll = VkBotLongPoll(vk_session, '193813979')


def main():
    status = 0
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            if status == 0:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Что вы хотите узнать?",
                                 random_id=random.randint(0, 2 ** 64))
                status = 1
            elif status == 1:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=wikipedia.summary(event.obj.message['text']),
                                 random_id=random.randint(0, 2 ** 64))
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Что вы хотите узнать?",
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()