#######################模組#######################
import asyncio
import discord
import os
import requests
from dotenv import load_dotenv
from AI.ai import Weather_API, AIAssistant

#######################初始化#######################
load_dotenv()

asyncio.set_event_loop(asyncio.new_event_loop())

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

weather_api = Weather_API(os.getenv("WEATHER_API_KEY"))
ai_assistant =AIAssistant(os.getenv("OPENAI_API_KEY"))

def build_weather_embed(weather_summary):
    """把整理好的天氣摘要排成 Discord 卡片"""
    embed = discord.Embed(
        title=f"{weather_summary['city_name']} 的天氣",
        description=f"敘述:{weather_summary['description']}",
        color=discord.Color.from_str("#7C08086C"),
    )
    icon_url = weather_api.get_icon_url(weather_summary["icon_code"])
    embed.set_thumbnail(url=icon_url)

    embed.add_field(
        name="溫度", value=f"{weather_summary['temperature_celsius']} °C", inline=False
    )
    return embed


def build_forecast_embeds(forecast_summaries):
    """把整理好的天氣預報摘要排成多張 Discord 卡片"""
    embeds = []
    for summary in forecast_summaries:
        embed = discord.Embed(
            title=f"{summary['city_name']} 的天氣預報-{summary['datetime']}",
            description=f"敘述:{summary['description']}",
            color=discord.Color.from_str("#00FAD0"),
        )
        icon_url = weather_api.get_icon_url(summary["icon_code"])
        embed.set_thumbnail(url=icon_url)
        embed.add_field(
            name="溫度", value=f"{summary['temperature_celsius']} °C", inline=False
        )
        embeds.append(embed)
    return embeds


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
async def weather(interaction: discord.Interaction, city: str, forecast: bool = False, ai: bool = False):
    """輸入/weather [城市名稱]，就會回覆該城市的天氣"""
    await interaction.response.defer()  # 先回覆一個「正在處理中」的訊息
    city_name = city.strip()
    if not weather_api.api_key:
        await interaction.followup.send(
            "尚未設定 WEATHER_API_KEY ,請先在 .env 檔案中完成設定。"
        )
        return
    try:
        if not forecast:
            weather_summary = weather_api.get_weather_summary(city)
            if weather_summary is None:
                await interaction.followup.send(
                    f"找不到城市 {city_name} 的天氣資訊，請確認城市名稱是否正確。"
                )
                return
            embed = build_weather_embed(weather_summary)
            await interaction.followup.send(embed=embed)
            return
        if not ai:
            forecast_summary = weather_api.get_forecast_summary(city)
            if forecast_summary is None:
                await interaction.followup.send(
                f"找不到城市 {city_name} 的天氣預報資訊，請確認城市名稱是否正確。")
                return
            embeds = build_forecast_embeds(forecast_summary)
            await interaction.followup.send(embeds=embeds[:10])  # Discord 一次最多只能發送 10 張卡片
            return
        
        #取得天氣預報原始資料的基本流程可參考
        raw_forecast = weather_api.get_forecast(city)
     
    except (requests.RequestException, ValueError):
        await interaction.followup.send("目前無法取得天氣資訊，請稍後再試。")
        return
    
    analysis, error = ai_assistant.ask(
        system_prompt="你是一個講話超欠揍的氣象分析師。",
        user_prompt=f"以下是{city_name}未來幾天的天氣預報資料，請根據這些數據提供詳細的分析和解釋：\n{raw_forecast}",
    )
    if error:
        await interaction.followup.send(f"AI分析時發生錯誤：{error}")
    else:
        await interaction.followup.send(f"AI分析結果：\n{analysis}")
    
#######################啟動#######################
def main():
    token = os.getenv("DC_BOT_TOKEN")
    bot.run(token)


if __name__ == "__main__":
    main()
