import vk_api
import os

LOGIN = ''
PASSWORD = ''
files = list(map(lambda x: f'static/img/{x}', os.listdir('static/img')))
login, password = LOGIN, PASSWORD
vk_session = vk_api.VkApi(login, password)
vk_session.auth(token_only=True)
upload  = vk_api.VkUpload(vk_session)
photo = upload.photo_wall(files)
vk_photo_id = [f"photo{i['owner_id']}_{i['id']}" for i in photo]
vk = vk_session.get_api()
vk.wall.post(message="Test", attachments=vk_photo_id)