import disnake
from discord.ext import commands, tasks
import platform
import asyncio
import os
import json

config_file_path = "config.json"

if not os.path.exists(config_file_path):
    config_data = {
        "TOKEN": "your_token_here",
        "YOU_ID": 123456789,
        "GUILD_ID": 123456789
    }
    with open(config_file_path, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)

with open(config_file_path, "r") as config_file:
    config = json.load(config_file)

token = config["TOKEN"]
guild_id = config["GUILD_ID"]
you = config["YOU_ID"]
bot = commands.Bot(command_prefix="!", intents=disnake.Intents.all())

@bot.event
async def on_ready():
    print('===============================================')
    print("The bot is ready!")
    print(f'Logged in as {bot.user.name}#{bot.user.discriminator} | {bot.user.id}')
    print(f'Running on {platform.system()} {platform.release()} ({os.name})')
    print(f'Bot version: {config.get("bot_version", "")}')
    print(f"Disnake version : {disnake.__version__}")
    print(f"Python version: {platform.python_version()}")
    print('===============================================')

async def load_cogs() -> None:
    for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                bot.logger.info(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                bot.logger.error(f"Failed to load extension {extension}\n{exception}")


asyncio.run(load_cogs())
bot.run(token)