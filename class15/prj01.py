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

CHANNEL_HISTORY_LIMIT = 15  # 定義要讀取的頻道歷史訊息數量
# system_prompt 像是給 AI 的角色卡，會影響 AI 回覆的語氣和工作方式。
CHAT_SYSTEM_PROMPT = """
你是一個講話讓人被嗆到說不出話來
你也會常常使用一些讓人聽了會想打人的詞彙
你還會罵人是白癡、智障、笨蛋、腦殘、弱智、傻子、白痴、蠢貨、三八、四肢發達腦子簡單的傢伙、幹、你媽、幹你娘
請根據頻道歷史判斷大家正在討論什麼，再回答最新提到你的問題。
回覆請使用繁體中文，語氣自然、簡短、適合國小學生閱讀。
如果頻道歷史不足以判斷答案，請說明你還需要哪一個資訊。
如果需要提到特定使用者或其他 bot，請複製歷史訊息裡的 mention：<@使用者ID>。
使用 mention 時，請直接放在一般文字中，不要寫成 @名字，也不要加反斜線、反引號或程式碼區塊。
不要使用 @everyone、@here 或角色標記，也不要自己編造 mention ID。
"""
AI_REPLY_ALLOWED_MENTIONS = discord.AllowedMentions(
    everyone=False,
    users=True,
    roles=False,
    replied_user=True,
)  
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
async def get_channel_history(channel, bot_user, limit=15, before=None):
    old_messages = []
    history_messages = []
    async for old_message in channel.history(
        limit=limit,
        before=before,
        oldest_first=False,
    ):
        old_messages.append(old_message)
    for message in old_messages:
        content = old_message.content.strip()
        if not content:
            continue
        if old_message.author == bot_user.id:
            history_messages.append({"role": "assistant", "content": content})
        else:
            speaker_type = "機器人"if old_message.author.bot else "同學"
            speaker_mention = old_message.author.mention
            user_content = (
                f"{old_message.author.display_name}"
                f"({speaker_type}，mention: {speaker_mention})說：{content}"
            )
def build_forecast_embeds(forecast_summaries):
    """把整理好的天氣預報摘要排成多張 Discord 卡片"""
    embeds = []
    for summary in forecast_summaries:
        embed = discord.Embed(
            title=f"{summary['city_name']} 的天氣預報-{summary['datetime']}",
            description=f"敘述:{summary['description']}",
            color=discord.Color.from_str("#757575"),
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
