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
asyncio.set_event_loop(asyncio.new_event_loop())

#######################事件#######################

#######################指令#######################

#######################啟動#######################
