import requests

API_KEY = "892da2f13edf3c7f382637760e72d224"
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast?"
UNITS = "metric"  # 使用公制單位（攝氏度）
LANG = "zh_tw"  # 使用中文

city = "Taipei"  # 預設城市

send_url = f"{BASE_URL}q={city}&appid={API_KEY}&units={UNITS}&lang={LANG}"

print(send_url)

response = requests.get(send_url)

info = response.json()

if "city" in info:
    for forecast in info["list"]:
        dt_txt = forecast["dt_txt"]
        temp = forecast["main"]["temp"]
        description = forecast["weather"][0]["description"]

        print(f"{dt_txt}: {temp}°C, {description}")
else:
    print("da sa bi")
