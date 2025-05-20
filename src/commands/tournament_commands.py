import discord
from discord.ext import commands
from discord import app_commands
import os
import json

def setup_tournament_commands(bot):
    @bot.tree.command(name="create_tournament", description="Erstellt ein neues Turnier")
    @app_commands.checks.has_permissions(administrator=True)
    async def create_tournament(interaction: discord.Interaction, name: str, team_size: int):
        guild_id = interaction.guild.id
        tournament_path = f'data/{guild_id}/{name}'
        if os.path.exists(tournament_path):
            await interaction.response.send_message(f'❌ Das Turnier "{name}" existiert bereits!', ephemeral=True)
            return
        os.makedirs(tournament_path, exist_ok=True)
        config = {
            "name": name,
            "status": "created",
            "created_by": interaction.user.id,
            "team_size": team_size
        }
        with open(f"{tournament_path}/config.json", "w") as f:
            json.dump(config, f)
        await interaction.response.send_message(f'✅ Turnier "{name}" wurde erstellt mit Teamgröße {team_size}!', ephemeral=True)

    @bot.tree.command(name="start_tournament", description="Startet ein Turnier")
    @app_commands.checks.has_permissions(administrator=True)
    async def start_tournament(interaction: discord.Interaction, name: str):
        guild_id = interaction.guild.id
        config_path = f'data/{guild_id}/{name}/config.json'
        players_path = f'data/{guild_id}/{name}/players.json'
        if not os.path.exists(config_path):
            await interaction.response.send_message(f'❌ Turnier "{name}" existiert nicht!', ephemeral=True)
            return
        if not os.path.exists(players_path):
            await interaction.response.send_message(f'❌ Keine Teilnehmer für "{name}" gefunden!', ephemeral=True)
            return
        with open(config_path, "r") as f:
            config = json.load(f)
        if config.get("status") == "started":
            await interaction.response.send_message(f'⚠️ Turnier "{name}" läuft bereits!', ephemeral=True)
            return
        config["status"] = "started"
        with open(config_path, "w") as f:
            json.dump(config, f)
        await interaction.response.send_message(f'🏁 Turnier "{name}" wurde gestartet!', ephemeral=True)

    @bot.tree.command(name="end_tournament", description="Beendet ein Turnier")
    @app_commands.checks.has_permissions(administrator=True)
    async def end_tournament(interaction: discord.Interaction, name: str):
        guild_id = interaction.guild.id
        config_path = f'data/{guild_id}/{name}/config.json'
        if not os.path.exists(config_path):
            await interaction.response.send_message(f'❌ Turnier "{name}" existiert nicht!', ephemeral=True)
            return
        with open(config_path, "r") as f:
            config = json.load(f)
        if config.get("status") == "ended":
            await interaction.response.send_message(f'⚠️ Turnier "{name}" ist bereits beendet!', ephemeral=True)
            return
        config["status"] = "ended"
        with open(config_path, "w") as f:
            json.dump(config, f)
        await interaction.response.send_message(f'🏁 Turnier "{name}" wurde beendet!', ephemeral=True)

    @bot.tree.command(name="delete_tournament", description="Löscht ein Turnier")
    @app_commands.checks.has_permissions(administrator=True)
    async def delete_tournament(interaction: discord.Interaction, name: str):
        import shutil
        guild_id = interaction.guild.id
        path = f'data/{guild_id}/{name}'
        if not os.path.exists(path):
            await interaction.response.send_message(f'❌ Turnier "{name}" existiert nicht!', ephemeral=True)
            return
        shutil.rmtree(path)
        await interaction.response.send_message(f'🗑️ Turnier "{name}" wurde gelöscht!', ephemeral=True)

    @bot.tree.command(name="reset_tournament", description="Setzt die Teilnehmerliste eines Turniers zurück")
    @app_commands.checks.has_permissions(administrator=True)
    async def reset_tournament(interaction: discord.Interaction, name: str):
        guild_id = interaction.guild.id
        path = f'data/{guild_id}/{name}/players.json'
        if os.path.exists(path):
            os.remove(path)
            await interaction.response.send_message(f'Teilnehmerliste für "{name}" wurde zurückgesetzt!', ephemeral=True)
        else:
            await interaction.response.send_message(f'Keine Teilnehmerliste für "{name}" gefunden!', ephemeral=True)

    @bot.tree.command(name="list_tournaments", description="Zeigt alle Turniere")
    async def list_tournaments(interaction: discord.Interaction):
        guild_id = interaction.guild.id
        path = f'data/{guild_id}/'
        if not os.path.exists(path):
            await interaction.response.send_message("ℹ️ Keine Turniere gefunden!", ephemeral=True)
            return
        tournaments = []
        for d in os.listdir(path):
            config_path = os.path.join(path, d, "config.json")
            if os.path.isdir(os.path.join(path, d)) and os.path.exists(config_path):
                with open(config_path, "r") as f:
                    config = json.load(f)
                tournaments.append(f'**{config["name"]}** (Status: {config.get("status", "unbekannt")})')
        if not tournaments:
            await interaction.response.send_message("ℹ️ Keine Turniere gefunden!", ephemeral=True)
            return
        await interaction.response.send_message("**Aktive Turniere:**\n" + "\n".join(tournaments), ephemeral=True)

    @bot.tree.command(name="help", description="Zeigt alle Befehle und Hilfe an")
    async def help_command(interaction: discord.Interaction):
        help_text = (
            "**Tourney Bot Slash-Befehle:**\n"
            "/create_tournament – Turnier erstellen (Admin)\n"
            "/start_tournament – Turnier starten (Admin)\n"
            "/end_tournament – Turnier beenden (Admin)\n"
            "/list_tournaments – Zeigt alle Turniere\n"
            "/ping – Bot-Status\n"
            # ...weitere Slash-Befehle hier ergänzen...
        )
        await interaction.response.send_message(help_text, ephemeral=True)

    @bot.tree.command(name="ping", description="Prüft, ob der Bot online ist")
    async def ping_command(interaction: discord.Interaction):
        await interaction.response.send_message("🏓 Pong! Der Bot ist online.", ephemeral=True)