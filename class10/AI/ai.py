import requests


class Weather_API:
    def __init__(self, api_key, lang="zh_tw"):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather?"
        self.units = "metric"
        self.lang = lang
        self.icon_base_url = "http://openweathermap.org/img/wn/"

    def get_current_weather(self, city_name):
        send_url = (
            self.base_url
            + "appid="
            + self.api_key
            + "&q="
            + city_name
            + "&units="
            + self.units
            + "&lang="
            + self.lang
        )
        response = requests.get(send_url)
        return response.json()

    def get_icon_url(self, icon_code):
        return self.icon_base_url + icon_code + "@4x.png"


# if "weather" in into and "main" in into:
#     weather = into["weather"][0]["description"]
#     temp = into["main"]["temp"]
#     icon_code = into["weather"][0]["icon"]
#     print("天氣:", weather)
#     print("溫度:", temp, "°C")
