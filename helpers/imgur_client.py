from imgurpython import ImgurClient
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from constants.secrets import IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET
import os

def load_client():
    client_id = IMGUR_CLIENT_ID
    client_secret = IMGUR_CLIENT_SECRET
    img_client = ImgurClient(client_id, client_secret)
    return img_client

def upload_image(file):
    img_client = load_client()
    file_name = default_storage.save(file.name, file)
    file = default_storage.open(file_name)
    file_url = "." + default_storage.url(file_name)
    try:
        res = img_client.upload_from_path(file_url, config=None, anon=False)
        default_storage.delete(file_name)
    except Exception as e:
        default_storage.delete(file_name)
        raise e 
    # print(res)
    print(res["link"])
    file_url = res["link"]
    _, file_extension = os.path.splitext(file_url)
    if file_extension == ".mp4":
        file_extension = True
    else:
        file_extension = False
    print("File uploaded and deleted")
    return file_url, file_extension


def upload_image_url(url, img_client):
    try:
        res = img_client.upload_from_url(url, config=None, anon=False)
        url = res["link"]
    except Exception as e:
        raise e 
    print("File uploaded and deleted")
    return url
