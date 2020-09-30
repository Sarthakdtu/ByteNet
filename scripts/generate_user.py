import requests, json

url = 'https://randomuser.me/api/'
def get_random_user():
    person = None
    try:
        res = requests.get(url)
        person = res.json()['results'][0]
        person = {
            "username":person["login"]["username"], 
            "password":person["login"]["password"]+" Bot", 
            "first":person["name"]["first"], 
            "last":person["name"]["last"],
            "email":person["email"],
            "location":person["location"]["city"],
            "age":person["dob"]["age"],
        }
        person["profile_pic_url"] = "https://avatars.dicebear.com/api/avataaars/"+person["username"]+".svg"
    except Exception as e:
        pass
    return person