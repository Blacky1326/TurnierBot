import discord
from discord import app_commands

def setup_admin_commands(bot):
    @bot.tree.command(name="set_admin_role", description="Setzt die Admin-Rolle für den Bot")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_admin_role(interaction: discord.Interaction, role: discord.Role):
        await interaction.response.send_message(f"Admin-Rolle auf {role.mention} gesetzt! (Platzhalter)", ephemeral=True)

    @bot.tree.command(name="set_language", description="Setzt die Sprache des Bots")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_language(interaction: discord.Interaction, language: str):
        await interaction.response.send_message(f"Sprache auf '{language}' gesetzt! (Platzhalter)", ephemeral=True)

    @bot.tree.command(name="set_branding", description="Setzt das Branding des Bots")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_branding(interaction: discord.Interaction, branding: str):
        await interaction.response.send_message(f"Branding auf '{branding}' gesetzt! (Platzhalter)", ephemeral=True)