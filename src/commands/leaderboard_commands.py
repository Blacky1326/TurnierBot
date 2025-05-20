import discord
from discord import app_commands

def setup_leaderboard_commands(bot):
    @bot.tree.command(name="leaderboard_create", description="Erstellt ein neues Leaderboard")
    @app_commands.checks.has_permissions(administrator=True)
    async def leaderboard_create(interaction: discord.Interaction, name: str):
        await interaction.response.send_message(f"Leaderboard '{name}' erstellt! (Platzhalter)", ephemeral=True)

    @bot.tree.command(name="leaderboard_config", description="Konfiguriert ein Leaderboard")
    @app_commands.checks.has_permissions(administrator=True)
    async def leaderboard_config(interaction: discord.Interaction, name: str):
        await interaction.response.send_message(f"Leaderboard '{name}' konfiguriert! (Platzhalter)", ephemeral=True)

    @bot.tree.command(name="leaderboard_link", description="Verknüpft ein Leaderboard mit einem Turnier")
    @app_commands.checks.has_permissions(administrator=True)
    async def leaderboard_link(interaction: discord.Interaction, leaderboard_name: str, tournament_name: str):
        await interaction.response.send_message(f"Leaderboard '{leaderboard_name}' mit Turnier '{tournament_name}' verknüpft! (Platzhalter)", ephemeral=True)