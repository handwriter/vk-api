from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import requests
from auth import TOKEN


vk_session = VkApi(token=TOKEN)
longpoll = VkBotLongPoll(vk_session, '193813979')


def main():
    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            request = requests.get(f'https://api.vk.com/method/users.get?user_ids={event.obj.message["from_id"]}&fields=city&access_token={TOKEN}&v=5.103').json()
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=f"Привет, {request['response'][0]['first_name']}",
                             random_id=random.randint(0, 2 ** 64))
            if 'city' in request['response'][0]:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Как поживает город {request['response'][0]['city']['title']}",
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()