from config import API_BASE_URL, API_KEY
import requests

def get_langs():
    response = requests.get(f'{API_BASE_URL}/getLangs', params={
        'key': API_KEY
    })
    return response.json()

def lookup(lang: str, text: str, ui: str='ru'):
    response = requests.get(f'{API_BASE_URL}/lookup', params={
        'key': API_KEY,
        'lang': lang,
        'text': text,
        'ui': ui
    })
    return response.json()

def display(json: dict) -> str:
    if json["def"] == [ ]:
        display = "Такого слова нет в словаре"
    else:
        display = f'{json["def"][0]["text"]} - {json["def"][0]["tr"][0]["text"]}'
    
    return display

