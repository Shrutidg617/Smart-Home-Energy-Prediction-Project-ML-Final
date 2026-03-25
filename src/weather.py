import requests

API_KEY = "762daef45ac39f4e15f96f84408127fc"

def get_weather(city="Nashik"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        res = requests.get(url).json()
        temp = res['main']['temp']
        humidity = res['main']['humidity']
    except:
        temp, humidity = 25, 50  # fallback

    return temp, humidity