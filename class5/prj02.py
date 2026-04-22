#######################匯入模組#######################
import requests
import os
import sys

os.chdir(sys.path[0])
#######################定義函數########################
API_KEY = "892da2f13edf3c7f382637760e72d224"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
UNITS = "metric"
LANG = "zh_tw"
ICON_URL = "http://openweathermap.org/img/wn/"
#######################主程式########################
city_name = "taipei"
send_url = (
    BASE_URL
    + "appid="
    + API_KEY
    + "&q="
    + city_name
    + "&units="
    + UNITS
    + "&lang="
    + LANG
)
print(send_url)
response = requests.get(send_url)  # 拿到json字串資料
into = response.json()  # 拿到字典資料

if "weather" in into and "main" in into:
    weather = into["weather"][0]["description"]
    temp = into["main"]["temp"]
    icon_code = into["weather"][0]["icon"]
    print("天氣:", weather)
    print("溫度:", temp, "°C")

    icon_url = ICON_URL + icon_code + "@4x.png"
    print("圖示URL:", icon_url)
    icon_response = requests.get(icon_url)
    if icon_response.status_code == 200:
        with open("gugugaga.png", "wb") as f:
            f.write(icon_response.content)
        print("圖示已下載並保存為 weather_icon.png")
    else:
        print("你是傻b嗎? 好像是吧......", icon_response.status_code)
else:
    print("你是傻b嗎? 好像是吧......")
