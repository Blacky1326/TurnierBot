import discord
from discord import app_commands
import os
import json

def setup_tournament_admin_commands(bot):
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

    @bot.tree.command(name="set_ranks", description="Setzt erlaubte Ränge für ein Turnier")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_ranks(interaction: discord.Interaction, tournament_name: str, ranks: str):
        guild_id = interaction.guild.id
        config_path = f'data/{guild_id}/{tournament_name}/config.json'
        if not os.path.exists(config_path):
            await interaction.response.send_message(f'Turnier "{tournament_name}" existiert nicht!', ephemeral=True)
            return
        with open(config_path, "r") as f:
            config = json.load(f)
        config["ranks"] = [r.strip() for r in ranks.split(",")]
        with open(config_path, "w") as f:
            json.dump(config, f)
        await interaction.response.send_message(f"Ranks für '{tournament_name}' gesetzt: {', '.join(config['ranks'])}", ephemeral=True)

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

    @bot.tree.command(name="admin_create", description="Setzt die Admin-Rolle für Turniere")
    @app_commands.checks.has_permissions(administrator=True)
    async def admin_create(interaction: discord.Interaction, role: discord.Role):
        guild_id = interaction.guild.id
        path = f'data/{guild_id}/admin_role.json'
        with open(path, "w") as f:
            json.dump({"role_id": role.id}, f)
        await interaction.response.send_message(f"Admin-Rolle für Turniere ist jetzt: {role.mention}", ephemeral=True)

    @bot.tree.command(name="language", description="Setzt die Sprache für den Server")
    @app_commands.checks.has_permissions(administrator=True)
    async def language(interaction: discord.Interaction, lang: str):
        guild_id = interaction.guild.id
        path = f'data/{guild_id}/language.json'
        with open(path, "w") as f:
            json.dump({"language": lang}, f)
        await interaction.response.send_message(f"Sprache für diesen Server gesetzt auf: {lang}", ephemeral=True)

    @bot.tree.command(name="branding", description="Setzt Branding-Informationen")
    @app_commands.checks.has_permissions(administrator=True)
    async def branding(interaction: discord.Interaction, infos: str):
        guild_id = interaction.guild.id
        path = f'data/{guild_id}/branding.txt'
        with open(path, "w", encoding="utf-8") as f:
            f.write(infos)
        await interaction.response.send_message("Branding-Informationen gespeichert!", ephemeral=True)