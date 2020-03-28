import vk_api
from datetime import datetime

LOGIN = ''
PASSWORD = ''
def main():
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    # Используем метод wall.get
    response = vk.wall.get(count=5)
    if response['items']:
        for i in response['items']:
            print(f'{i["text"]};')
            print(f'date: {datetime.fromtimestamp(i["date"]).date()}, time: {datetime.fromtimestamp(i["date"]).time()};')


if __name__ == '__main__':
    main()