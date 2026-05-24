#######################模組#######################
import asyncio
import discord
import os
import requests
from dotenv import load_dotenv
from AI.ai import Weather_API

#######################初始化#######################
load_dotenv()
asyncio.set_event_loop(asyncio.new_event_loop())
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)
weather_api = Weather_API(os.getenv("WEATHER_API_KEY"))


def build_weather_embed(weather_summary):
    """把整理好的天氣摘要排成 Discord 卡片"""
    embed = discord.Embed(
        title=f"{weather_summary['city_name']} 的天氣",
        description=f"敘述:{weather_summary['description']}",
        color=discord.Color.from_str("#1E90FF"),
    )
    icon_url = weather_api.get_icon_url(weather_summary["icon_code"])
    embed.set_thumbnail(url=icon_url)

    embed.add_field(
        name="溫度", value=f"{weather_summary['temperature_celsius']} °C", inline=False
    )
    return embed


#######################事件#######################
@bot.event
async def on_ready():
    await tree.sync()  # 送列表給discord機器人
    print(f"已登入 {bot.user}")  # 說已經開啟了


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "hello":
        await message.channel.send("大帥比")


#######################指令#######################
@tree.command(name="hi", description="say hello")
async def hi(interaction: discord.Interaction):
    await interaction.response.send_message("大帥比")


@tree.command(name="weather", description="查詢天氣")
async def weather(interaction: discord.Interaction, city: str):
    """輸入/weather [城市名稱]，就會回覆該城市的天氣"""
    await interaction.response.defer()  # 先回覆一個「正在處理中」的訊息
    city_name = city.strip()

    if not weather_api.api_key:
        await interaction.followup.send(
            "尚未設定 WEATHER_API_KEY ,請先在 .env 檔案中完成設定。"
        )
        return
    try:
        weather_summary = weather_api.get_weather_summary(city)
    except (requests.RequestException, ValueError):
        await interaction.followup.send("目前無法取得天氣資訊，請稍後再試。")
        return
    if weather_summary is None:
        await interaction.followup.send(
            f"找不到城市 {city_name} 的天氣資訊，請確認城市名稱是否正確。"
        )
        return
    embed = build_weather_embed(weather_summary)
    await interaction.followup.send(embed=embed)


#######################啟動#######################
def main():
    token = os.getenv("DC_BOT_TOKEN")
    bot.run(token)


if __name__ == "__main__":
    main()
