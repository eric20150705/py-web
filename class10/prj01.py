#######################模組#######################
import asyncio
import discord
import os
from dotenv import load_dotenv

#######################初始化#######################
load_dotenv()
asyncio.set_event_loop(asyncio.new_event_loop())
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)


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


#######################啟動#######################
def main():
    token = os.getenv("DC_BOT_TOKEN")
    bot.run(token)


if __name__ == "__main__":
    main()
