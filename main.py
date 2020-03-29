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
    response = response = vk.friends.get(fields="first_name, last_name, bdate")
    if response['items']:
        for i in sorted(response['items'], key=lambda x: x['last_name']):
            print(i['last_name'], i['first_name'], end=' ')
            a = ''
            if 'bdate' in i:
                a = i['bdate']
            print(a)


if __name__ == '__mai n__':
    main()