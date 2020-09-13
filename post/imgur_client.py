from imgurpython import ImgurClient
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from constants.secrets import IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET

def load_client():
    client_id = IMGUR_CLIENT_ID
    client_secret = IMGUR_CLIENT_SECRET
    img_client = ImgurClient(client_id, client_secret)
    return img_client

def upload_image(file):
    img_client = load_client()
    file_name = default_storage.save(file.name, file)
    file = default_storage.open(file_name)
    file_url = "./media" + default_storage.url(file_name)
    # fs = FileSystemStorage(location='/media/')
    # filename = fs.save(file.name, file)
    # file_url = fs.url(filename)
    # print(file_url)
    try:
        res = img_client.upload_from_path(file_url, config=None, anon=False)
    except Exception as e:
        raise e
    default_storage.delete(file_name)
    # print(res)
    print(res["link"])
    print("File uploaded and deleted")
    return res["link"]

