import json

def get_token():
    with open("config.json", 'r') as file:
        data = json.loads(file.read())
    return data["token"]



print(get_token())