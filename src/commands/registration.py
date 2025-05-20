import discord
from discord import app_commands
import os
import json

def setup_registration_commands(bot):
    @bot.tree.command(name="register", description="Registriere dich für ein Turnier")
    async def register(interaction: discord.Interaction, tournament_name: str, ign: str, rank: str):
        guild_id = interaction.guild.id
        user_id = str(interaction.user.id)
        config_path = f'data/{guild_id}/{tournament_name}/config.json'
        players_path = f'data/{guild_id}/{tournament_name}/players.json'
        if not os.path.exists(config_path):
            await interaction.response.send_message(f'Turnier "{tournament_name}" existiert nicht!', ephemeral=True)
            return
        with open(config_path, "r") as f:
            config = json.load(f)
        allowed_ranks = config.get("ranks", [])
        if allowed_ranks and rank not in allowed_ranks:
            await interaction.response.send_message(f"Ungültiger Rank! Erlaubt: {', '.join(allowed_ranks)}", ephemeral=True)
            return
        players = {}
        if os.path.exists(players_path):
            with open(players_path, "r") as f:
                players = json.load(f)
        if user_id in players:
            await interaction.response.send_message("Du bist bereits registriert!", ephemeral=True)
            return
        players[user_id] = {"ign": ign, "rank": rank}
        with open(players_path, "w") as f:
            json.dump(players, f)
        await interaction.response.send_message(f"{interaction.user.mention} ist für '{tournament_name}' registriert mit IGN '{ign}' und Rank '{rank}'!", ephemeral=True)

    @bot.tree.command(name="unregister", description="Melde dich von einem Turnier ab")
    async def unregister(interaction: discord.Interaction, tournament_name: str):
        guild_id = interaction.guild.id
        user_id = str(interaction.user.id)
        players_path = f'data/{guild_id}/{tournament_name}/players.json'
        if not os.path.exists(players_path):
            await interaction.response.send_message(f'Teilnehmerliste für "{tournament_name}" nicht gefunden!', ephemeral=True)
            return
        with open(players_path, "r") as f:
            players = json.load(f)
        if user_id not in players:
            await interaction.response.send_message("Du bist nicht registriert!", ephemeral=True)
            return
        players.pop(user_id)
        with open(players_path, "w") as f:
            json.dump(players, f)
        await interaction.response.send_message(f"{interaction.user.mention} wurde aus '{tournament_name}' entfernt!", ephemeral=True)

    @bot.tree.command(name="kick", description="Entfernt einen Spieler aus einem Turnier")
    @app_commands.checks.has_permissions(administrator=True)
    async def kick(interaction: discord.Interaction, tournament_name: str, player_id: str):
        guild_id = interaction.guild.id
        players_path = f'data/{guild_id}/{tournament_name}/players.json'
        if not os.path.exists(players_path):
            await interaction.response.send_message(f'Teilnehmerliste für "{tournament_name}" nicht gefunden!', ephemeral=True)
            return
        with open(players_path, "r") as f:
            players = json.load(f)
        if player_id not in players:
            await interaction.response.send_message(f"Spieler mit ID {player_id} ist nicht registriert!", ephemeral=True)
            return
        players.pop(player_id)
        with open(players_path, "w") as f:
            json.dump(players, f)
        await interaction.response.send_message(f"Spieler mit ID {player_id} wurde aus '{tournament_name}' entfernt!", ephemeral=True)

    @bot.tree.command(name="unkick", description="Fügt einen Spieler wieder zu einem Turnier hinzu")
    @app_commands.checks.has_permissions(administrator=True)
    async def unkick(interaction: discord.Interaction, tournament_name: str, player_id: str):
        guild_id = interaction.guild.id
        players_path = f'data/{guild_id}/{tournament_name}/players.json'
        if not os.path.exists(players_path):
            await interaction.response.send_message(f'Teilnehmerliste für "{tournament_name}" nicht gefunden!', ephemeral=True)
            return
        with open(players_path, "r") as f:
            players = json.load(f)
        if player_id in players:
            await interaction.response.send_message(f"Spieler mit ID {player_id} ist bereits registriert!", ephemeral=True)
            return
        players[player_id] = {"ign": "Unbekannt", "rank": "Unbekannt"}
        with open(players_path, "w") as f:
            json.dump(players, f)
        await interaction.response.send_message(f"Spieler mit ID {player_id} wurde zu '{tournament_name}' hinzugefügt!", ephemeral=True)

    @bot.tree.command(name="rename", description="Benennt einen Spieler im Turnier um")
    @app_commands.checks.has_permissions(administrator=True)
    async def rename(interaction: discord.Interaction, tournament_name: str, player_id: str, new_name: str):
        guild_id = interaction.guild.id
        names_path = f'data/{guild_id}/{tournament_name}/names.json'
        names = {}
        if os.path.exists(names_path):
            with open(names_path, "r") as f:
                names = json.load(f)
        names[player_id] = new_name
        with open(names_path, "w") as f:
            json.dump(names, f)
        await interaction.response.send_message(f"Spieler mit ID {player_id} wurde zu '{new_name}' umbenannt in '{tournament_name}'!", ephemeral=True)

    @bot.tree.command(name="fake", description="Fügt Fake-Spieler zu einem Turnier hinzu")
    @app_commands.checks.has_permissions(administrator=True)
    async def fake(interaction: discord.Interaction, tournament_name: str, count: int):
        guild_id = interaction.guild.id
        players_path = f'data/{guild_id}/{tournament_name}/players.json'
        if not os.path.exists(players_path):
            await interaction.response.send_message(f'Teilnehmerliste für "{tournament_name}" nicht gefunden!', ephemeral=True)
            return
        with open(players_path, "r") as f:
            players = json.load(f)
        start_id = 100000000000000000  # Dummy-ID für Fake-Spieler
        for i in range(count):
            fake_id = f"fake_{start_id + len(players) + i}"
            players[fake_id] = {"ign": f"FakePlayer{len(players)+i+1}", "rank": "Unranked"}
        with open(players_path, "w") as f:
            json.dump(players, f)
        await interaction.response.send_message(f"{count} Fake-Spieler zu '{tournament_name}' hinzugefügt!", ephemeral=True)

    @bot.tree.command(name="leave", description="Verlasse ein Turnier")
    async def leave(interaction: discord.Interaction, tournament_name: str):
        guild_id = interaction.guild.id
        user_id = str(interaction.user.id)
        players_path = f'data/{guild_id}/{tournament_name}/players.json'
        if not os.path.exists(players_path):
            await interaction.response.send_message(f'Teilnehmerliste für "{tournament_name}" nicht gefunden!', ephemeral=True)
            return
        with open(players_path, "r") as f:
            players = json.load(f)
        if user_id not in players:
            await interaction.response.send_message("Du bist nicht registriert!", ephemeral=True)
            return
        players.pop(user_id)
        with open(players_path, "w") as f:
            json.dump(players, f)
        await interaction.response.send_message(f"{interaction.user.mention} hat '{tournament_name}' verlassen!", ephemeral=True)