import discord
from discord.ext import commands
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from commands.tournament_commands import setup_tournament_commands

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot ist online als {bot.user}")

@bot.event
async def on_guild_join(guild):
    os.makedirs(f'data/{guild.id}', exist_ok=True)

setup_tournament_commands(bot)

bot.run('YOUR_BOT_TOKEN')