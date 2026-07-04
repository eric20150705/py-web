import requests
import openai

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
class AIAssistant:
    """把OpenAI的對話功能整理成可重複使用的工具類別"""
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key
    def ask(
            self,
            system_prompt,
            user_prompt,
            history_messages=None,
            temperature=0.2,
            model="gpt-4o",
    ):
        #這個方法讓我們可以問AI一個問題，並得到一次性回答。
        #system_prompt 是給AI的角色設定，例如[你是氣象分析師]
        #user_message 是我們要問的具體問題，例如[請分析這段天氣預報資料]

        if not self.api_key:
            return "尚未設定 OpenAI API 金鑰，請先在 .env 檔案中完成設定。"
        if history_messages is None:
            history_messages = []

        messages = ([{"role": "system", "content": system_prompt}] 
                    + history_messages
                    + [{"role": "user", "content": user_prompt}]
                    )
        print("===向AI送出的訊息列表===")
        for msg in messages:
            print(f"{msg['role']}: {msg['content']}")
        print("==========================")
        try:
            #向AI送出請求
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
            )
            #取出AI的回答內容
            assistant_message = response.choices[0].message.content
            return assistant_message, None
        except Exception as e:
            return None, f"發生錯誤：{e}"