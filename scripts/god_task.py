import requests
url = "https://bytenet.pythonanywhere.com/home/god_script"
res = requests.get(url)
print(res.json())