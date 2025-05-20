import discord
from discord import app_commands
import os
import json

def setup_match_commands(bot):
    @bot.tree.command(name="score_group", description="Trage das Ergebnis eines Gruppen-Matches ein")
    @app_commands.checks.has_permissions(administrator=True)
    async def score_group(interaction: discord.Interaction, tournament_name: str, match_id: str, score_a: int, score_b: int):
        guild_id = interaction.guild.id
        config_path = f'data/{guild_id}/{tournament_name}/config.json'
        with open(config_path, "r") as f:
            config = json.load(f)
        if config.get("phase") != "group":
            await interaction.response.send_message("Dieser Command ist nur in der Gruppenphase erlaubt!", ephemeral=True)
            return

        matches_path = f'data/{guild_id}/{tournament_name}/group_matches.json'
        groups_path = f'data/{guild_id}/{tournament_name}/groups.json'
        if not os.path.exists(matches_path):
            await interaction.response.send_message("Gruppen-Matches nicht gefunden!", ephemeral=True)
            return

        with open(matches_path, "r") as f:
            matches = json.load(f)
        with open(groups_path, "r") as f:
            groups = json.load(f)

        match = next((m for m in matches if m["id"] == match_id), None)
        if not match:
            await interaction.response.send_message("Match-ID nicht gefunden!", ephemeral=True)
            return

        match["score_a"] = score_a
        match["score_b"] = score_b
        match["played"] = True

        with open(matches_path, "w") as f:
            json.dump(matches, f, indent=2)

        await interaction.response.send_message(f"Ergebnis für Gruppen-Match {match_id} eingetragen: {score_a}:{score_b}", ephemeral=False)

        # Prüfen, ob noch offene Matches existieren
        next_match = next((m for m in matches if not m.get("played")), None)
        if next_match:
            # Teamnamen und Spieler für die nächste Paarung posten
            def get_team_name(team_uids):
                for group in groups:
                    for idx, team in enumerate(group):
                        if sorted([uid for uid, _ in team]) == sorted(team_uids):
                            return "Team " + str(idx+1) + ": " + ", ".join(f"{ign} (<@{uid}>)" for uid, ign in team)
                return "Unbekanntes Team"

            team_a_str = get_team_name(next_match["team_a"])
            team_b_str = get_team_name(next_match["team_b"])
            await interaction.channel.send(f"Nächstes Gruppen-Match: {team_a_str} **vs** {team_b_str}\n(Match-ID: {next_match['id']})")
        else:
            await interaction.channel.send("**Alle Gruppenspiele sind abgeschlossen! Die K.O.-Phase kann gestartet werden.**")

    @bot.tree.command(name="score_ko", description="Trage das Ergebnis eines K.O.-Matches ein")
    @app_commands.checks.has_permissions(administrator=True)
    async def score_ko(interaction: discord.Interaction, tournament_name: str, match_index: int, score1: int, score2: int):
        guild_id = interaction.guild.id
        config_path = f'data/{guild_id}/{tournament_name}/config.json'
        with open(config_path, "r") as f:
            config = json.load(f)
        if config.get("phase") != "ko":
            await interaction.response.send_message("Dieser Command ist nur in der K.O.-Phase (außer Finale) erlaubt!", ephemeral=True)
            return

        ko_path = f'data/{guild_id}/{tournament_name}/ko_bracket.json'
        groups_path = f'data/{guild_id}/{tournament_name}/groups.json'
        if not os.path.exists(ko_path):
            await interaction.response.send_message("K.O.-Bracket nicht gefunden!", ephemeral=True)
            return

        with open(ko_path, "r") as f:
            ko_matches = json.load(f)
        with open(groups_path, "r") as f:
            groups = json.load(f)

        if match_index < 0 or match_index >= len(ko_matches):
            await interaction.response.send_message("Ungültiger Match-Index!", ephemeral=True)
            return

        match = ko_matches[match_index]

        # Prüfe, ob es das letzte Match ist (Finale)
        is_final = (match_index == len(ko_matches) - 1 and all(m.get("winner") for m in ko_matches[:-1]))
        if is_final:
            config["phase"] = "final"
            with open(config_path, "w") as f:
                json.dump(config, f)
            await interaction.response.send_message("Das Finale hat begonnen! Bitte benutze ab jetzt nur noch /final_win.", ephemeral=True)
            # Finale-Teams posten
            def get_team_name(team_id):
                for group in groups:
                    for idx, team in enumerate(group):
                        if f"G{groups.index(group)+1}_T{idx+1}" == team_id:
                            return "Team " + str(idx+1) + ": " + ", ".join(f"{ign} (<@{uid}>)" for uid, ign in team)
                return "Unbekanntes Team"
            team1_str = get_team_name(match["team1"])
            team2_str = get_team_name(match["team2"])
            await interaction.channel.send(f"**Finale:** {team1_str} **vs** {team2_str}")
            return

        # Normale K.O.-Runde
        match["score1"] = score1
        match["score2"] = score2
        if score1 > score2:
            match["winner"] = match["team1"]
        elif score2 > score1:
            match["winner"] = match["team2"]
        else:
            await interaction.response.send_message("Unentschieden ist in der K.O.-Phase nicht erlaubt!", ephemeral=True)
            return
        msg = f"Ergebnis für K.O.-Match {match_index+1} eingetragen!"

        # Nächste Runde automatisch erstellen, wenn alle dieser Runde fertig sind
        current_round = match["round"]
        finished_matches = [m for m in ko_matches if m["round"] == current_round and m.get("winner")]
        if len(finished_matches) * 2 == len([m for m in ko_matches if m["round"] == current_round]):
            winners = [m["winner"] for m in ko_matches if m["round"] == current_round]
            next_round = current_round + 1
            new_matches = []
            for i in range(0, len(winners), 2):
                if i+1 < len(winners):
                    new_matches.append({
                        "round": next_round,
                        "team1": winners[i],
                        "team2": winners[i+1],
                        "score1": None,
                        "score2": None,
                        "winner": None
                    })
            ko_matches.extend(new_matches)
            msg += " Nächste Runde erstellt."

        with open(ko_path, "w") as f:
            json.dump(ko_matches, f, indent=2)

        await interaction.response.send_message(msg, ephemeral=False)

        # Nächstes offenes K.O.-Match posten
        next_ko = next((m for m in ko_matches if m.get("winner") is None), None)
        if next_ko:
            def get_team_name(team_id):
                for group in groups:
                    for idx, team in enumerate(group):
                        if f"G{groups.index(group)+1}_T{idx+1}" == team_id:
                            return "Team " + str(idx+1) + ": " + ", ".join(f"{ign} (<@{uid}>)" for uid, ign in team)
                return "Unbekanntes Team"
            team1_str = get_team_name(next_ko["team1"])
            team2_str = get_team_name(next_ko["team2"])
            await interaction.channel.send(f"Nächstes K.O.-Match: {team1_str} **vs** {team2_str}")

    @bot.tree.command(name="final_win", description="Trägt einen Sieg im Best-of-3-Finale ein")
    @app_commands.checks.has_permissions(administrator=True)
    async def final_win(interaction: discord.Interaction, tournament_name: str, winner: int):
        guild_id = interaction.guild.id
        config_path = f'data/{guild_id}/{tournament_name}/config.json'
        with open(config_path, "r") as f:
            config = json.load(f)
        if config.get("phase") != "final":
            await interaction.response.send_message("Dieser Command ist nur im Finale erlaubt!", ephemeral=True)
            return

        ko_path = f'data/{guild_id}/{tournament_name}/ko_bracket.json'
        groups_path = f'data/{guild_id}/{tournament_name}/groups.json'
        if not os.path.exists(ko_path):
            await interaction.response.send_message("K.O.-Bracket nicht gefunden!", ephemeral=True)
            return

        with open(ko_path, "r") as f:
            ko_matches = json.load(f)

        # Das Finale ist immer das letzte Match im Bracket
        final = ko_matches[-1]
        if "final_wins_team1" not in final:
            final["final_wins_team1"] = 0
            final["final_wins_team2"] = 0

        if winner == 1:
            final["final_wins_team1"] += 1
        elif winner == 2:
            final["final_wins_team2"] += 1
        else:
            await interaction.response.send_message("Winner muss 1 (Team1) oder 2 (Team2) sein!", ephemeral=True)
            return

        # Prüfe, ob ein Team gewonnen hat
        if final["final_wins_team1"] == 2 or final["final_wins_team2"] == 2:
            final["winner"] = final["team1"] if final["final_wins_team1"] == 2 else final["team2"]
            # Teilnehmer auslesen
            if os.path.exists(groups_path):
                with open(groups_path, "r") as f:
                    groups = json.load(f)
                winner_id = final["winner"]
                winner_team = None
                for group in groups:
                    for idx, team in enumerate(group):
                        team_id = f"G{groups.index(group)+1}_T{idx+1}"
                        if team_id == winner_id:
                            winner_team = team
                            break
                if winner_team:
                    member_list = ", ".join(f"{ign} (<@{uid}>)" for uid, ign in winner_team)
                else:
                    member_list = "Unbekannt"
            else:
                member_list = "Unbekannt"
            msg = f"🏆 Das Finale ist entschieden!\n**Sieger-Team:** {final['winner']}\n**Mitglieder:** {member_list}"
        else:
            msg = f"Zwischenstand im Finale: Team1 {final['final_wins_team1']} Siege, Team2 {final['final_wins_team2']} Siege."

        with open(ko_path, "w") as f:
            json.dump(ko_matches, f, indent=2)

        await interaction.response.send_message(msg, ephemeral=False)