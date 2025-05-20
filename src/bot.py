import discord
from discord.ext import commands
import os
import sys

# Damit die Commands-Module gefunden werden
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from commands.tournament_commands import setup_tournament_commands
from commands.registration import setup_registration_commands
from commands.team_commands import setup_team_commands
from commands.match_commands import setup_match_commands
from commands.leaderboard_commands import setup_leaderboard_commands
from commands.admin_commands import setup_admin_commands

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

# Setup aller Command-Module
setup_tournament_commands(bot)
setup_registration_commands(bot)
setup_team_commands(bot)
setup_match_commands(bot)
setup_leaderboard_commands(bot)
setup_admin_commands(bot)

# Bot-Token aus Umgebungsvariable (empfohlen)
bot.run('YOUR_BOT_TOKEN')