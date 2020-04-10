from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import requests
from auth import TOKEN
from datetime import datetime


vk_session = VkApi(token=TOKEN)
longpoll = VkBotLongPoll(vk_session, '193813979')


def main():
    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            request = requests.get(f'https://api.vk.com/method/users.get?user_ids={event.obj.message["from_id"]}&fields=city&access_token={TOKEN}&v=5.103').json()
            if sum([1 for i in ['время', 'число', 'дата', 'день'] if i in event.obj.message['text']]) != 0:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=datetime.now(),
                                 random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Если в новом сообщении пользователя есть слова: «время», «число», «дата», «день», нужно сообщить ему сегодняшнюю дату, московское время и день недели.",
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()