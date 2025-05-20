import discord
from discord import app_commands
import os
import json
import random
from collections import defaultdict

def setup_team_commands(bot):
    @bot.tree.command(name="shuffle_teams", description="Teilt die Spieler fair in Teams und Gruppen ein")
    @app_commands.checks.has_permissions(administrator=True)
    async def shuffle_teams(interaction: discord.Interaction, tournament_name: str):
        guild_id = interaction.guild.id
        players_path = f'data/{guild_id}/{tournament_name}/players.json'
        config_path = f'data/{guild_id}/{tournament_name}/config.json'
        if not os.path.exists(players_path):
            await interaction.response.send_message(f'Keine Spieler für "{tournament_name}" gefunden!', ephemeral=True)
            return
        with open(players_path, "r") as f:
            players = json.load(f)
        with open(config_path, "r") as f:
            config = json.load(f)
        team_size = config.get("team_size", 5)
        num_players = len(players)
        num_teams = num_players // team_size
        if num_players % team_size != 0:
            num_teams += 1  # Restteam

        TEAM_NAMES = [
            "Löwen", "Tiger", "Adler", "Wölfe", "Bären", "Falken", "Panther", "Drachen",
            "Haie", "Eulen", "Pumas", "Kobras", "Phönixe", "Stiere", "Raben", "Eisbären",
            "Leoparden", "Geparden", "Krähen", "Mambas", "Mäuse", "Erdmännchen", "Pinguine", "Kojoten"
        ]
        random.shuffle(TEAM_NAMES)

        # Teams nach Rängen mischen
        rank_groups = defaultdict(list)
        for user_id, pdata in players.items():
            rank_groups[pdata["rank"]].append((user_id, pdata["ign"]))
        teams = [[] for _ in range(num_teams)]
        i = 0
        for rank in sorted(config.get("ranks", []), reverse=True):
            random.shuffle(rank_groups[rank])
            for player in rank_groups[rank]:
                teams[i % num_teams].append(player)
                i += 1

        # Teams in Gruppen aufteilen (z.B. 4 Gruppen)
        num_groups = 4
        groups = [[] for _ in range(num_groups)]
        for idx, team in enumerate(teams):
            groups[idx % num_groups].append(team)

        # Teams und Gruppen speichern + Teamnamen zuweisen
        groups_path = f'data/{guild_id}/{tournament_name}/groups.json'
        team_names_path = f'data/{guild_id}/{tournament_name}/team_names.json'
        team_names_dict = {}
        team_counter = 0
        for g_idx, group in enumerate(groups):
            for t_idx, team in enumerate(group):
                team_id = f"G{g_idx+1}_T{t_idx+1}"
                name = TEAM_NAMES[team_counter % len(TEAM_NAMES)]
                team_names_dict[team_id] = name
                team_counter += 1
        with open(groups_path, "w") as f:
            json.dump(groups, f)
        with open(team_names_path, "w") as f:
            json.dump(team_names_dict, f)

        # Phase auf Gruppenphase setzen
        config["phase"] = "group"
        with open(config_path, "w") as f:
            json.dump(config, f)

        # --- Gruppenphasen-Matches automatisch erstellen ---
        matches = []
        match_id = 1
        for group_idx, group in enumerate(groups):
            for team_a_idx in range(len(group)):
                for team_b_idx in range(team_a_idx + 1, len(group)):
                    team_a = group[team_a_idx]
                    team_b = group[team_b_idx]
                    matches.append({
                        "id": f"G{group_idx+1}_M{match_id}",
                        "group": group_idx + 1,
                        "team_a": [uid for uid, _ in team_a],
                        "team_b": [uid for uid, _ in team_b],
                        "score_a": None,
                        "score_b": None,
                        "played": False,
                        "team_a_id": f"G{group_idx+1}_T{team_a_idx+1}",
                        "team_b_id": f"G{group_idx+1}_T{team_b_idx+1}"
                    })
                    match_id += 1

        matches_path = f'data/{guild_id}/{tournament_name}/group_matches.json'
        with open(matches_path, "w") as f:
            json.dump(matches, f, indent=2)

        # Teams & Gruppen posten (mit Teamnamen)
        msg = f"**Teams & Gruppen für '{tournament_name}':**\n"
        for g_idx, group in enumerate(groups, 1):
            msg += f"\n__Gruppe {g_idx}:__\n"
            for t_idx, team in enumerate(group, 1):
                team_id = f"G{g_idx}_T{t_idx}"
                name = team_names_dict.get(team_id, f"Team {t_idx}")
                msg += f"{name}: " + ", ".join(f"{ign} (<@{uid}>)" for uid, ign in team) + "\n"
        msg += f"\n__Es wurden {len(matches)} Gruppenphasen-Matches automatisch erstellt!__\n"
        await interaction.response.send_message(msg, ephemeral=False)

        # Matches posten (mit Teamnamen)
        for match in matches:
            team_a_name = team_names_dict.get(match["team_a_id"], match["team_a_id"])
            team_b_name = team_names_dict.get(match["team_b_id"], match["team_b_id"])
            team_a_mentions = ", ".join(f"<@{uid}>" for uid in match["team_a"])
            team_b_mentions = ", ".join(f"<@{uid}>" for uid in match["team_b"])
            await interaction.channel.send(
                f"Match-ID: {match['id']} | **{team_a_name}** ({team_a_mentions}) vs **{team_b_name}** ({team_b_mentions})"
            )

    @bot.tree.command(name="seeds", description="Zeigt oder bearbeitet Seeds für ein Turnier")
    @app_commands.checks.has_permissions(administrator=True)
    async def seeds(interaction: discord.Interaction, tournament_name: str):
        await interaction.response.send_message(f"Seeds für '{tournament_name}' anzeigen/bearbeiten! (Platzhalter)", ephemeral=True)

    @bot.tree.command(name="team", description="Bearbeitet ein Team in einem Turnier")
    @app_commands.checks.has_permissions(administrator=True)
    async def team(interaction: discord.Interaction, tournament_name: str, team_name: str):
        await interaction.response.send_message(f"Team '{team_name}' in '{tournament_name}' bearbeitet! (Platzhalter)", ephemeral=True)