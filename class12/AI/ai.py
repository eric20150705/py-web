import requests


class Weather_API:
    def __init__(self, api_key, lang="zh_tw"):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather?"
        self.base_url_forecast = "https://api.openweathermap.org/data/2.5/forecast?"
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

    def get_weather_summary(self, city_name):
        info = self.get_current_weather(city_name)

        if "weather" in info and "main" in info:
            return {
                "city_name": info.get("name", city_name),
                "temperature_celsius": info["main"]["temp"],
                "description": info["weather"][0]["description"],
                "icon_code": info["weather"][0]["icon"],
            }
        return None

    def get_icon(self, icon_code):
        icon_url = self.get_icon_url(icon_code)
        response = requests.get(icon_url)
        if response.status_code == 200:
            return response.content
        return None

    def get_forecast(self, city_name):
        send_url = (
            self.base_url_forecast
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

    def get_forecast_summary(self, city_name, count=10):
        forecast_count = max(0, count)
        try:
            info = self.get_forecast(city_name)
        except requests.HTTPError as error:
            response = error.response
            if response is not None and response.status_code == 404:
                return None
            raise
        if "list" not in info or "city" not in info:
            return None
        city_label = info["city"].get("name", city_name)
        forecast_list = []

        for forecast in info["list"][:forecast_count]:
            forecast_list.append(
                {
                    "city_name": city_label,
                    "datetime": forecast.get("dt_txt", ""),
                    "temperature_celsius": forecast["main"].get("temp", 0),
                    "description": forecast["weather"][0].get("description", ""),
                    "icon_code": forecast["weather"][0].get("icon", ""),
                }
            )
        return forecast_list
