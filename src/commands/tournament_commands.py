import discord
from discord.ext import commands
from discord import app_commands
import os
import json
import random
from collections import defaultdict

async def create_tournament(ctx, name):
    guild_id = ctx.guild.id
    tournament_path = f'data/{guild_id}/{name}'
    if os.path.exists(tournament_path):
        await ctx.send(f'❌ Das Turnier "{name}" existiert bereits!')
        return
    os.makedirs(tournament_path, exist_ok=True)
    # Standard-Config anlegen
    config = {
        "name": name,
        "status": "created",
        "created_by": ctx.author.id
    }
    with open(f"{tournament_path}/config.json", "w") as f:
        json.dump(config, f)
    await ctx.send(f'✅ Turnier "{name}" wurde erstellt!')

async def start_tournament(ctx, name):
    guild_id = ctx.guild.id
    config_path = f'data/{guild_id}/{name}/config.json'
    players_path = f'data/{guild_id}/{name}/players.json'
    if not os.path.exists(config_path):
        await ctx.send(f'❌ Turnier "{name}" existiert nicht!')
        return
    if not os.path.exists(players_path):
        await ctx.send(f'❌ Keine Teilnehmer für "{name}" gefunden!')
        return
    with open(config_path, "r") as f:
        config = json.load(f)
    if config.get("status") == "started":
        await ctx.send(f'⚠️ Turnier "{name}" läuft bereits!')
        return
    config["status"] = "started"
    with open(config_path, "w") as f:
        json.dump(config, f)
    await ctx.send(f'🏁 Turnier "{name}" wurde gestartet!')

async def register_player(ctx, tournament_name, player_name):
    # Logic to register a player for a tournament
    await ctx.send(f'Player "{player_name}" registered for "{tournament_name}"!')

async def show_leaderboard(ctx, tournament_name):
    # Logic to show the leaderboard for a tournament
    await ctx.send(f'Leaderboard for "{tournament_name}": ...')

async def config_tournament(ctx, name, key, value):
    guild_id = ctx.guild.id
    path = f'data/{guild_id}/{name}/config.json'
    if not os.path.exists(f'data/{guild_id}/{name}'):
        await ctx.send(f'Turnier \"{name}\" existiert nicht!')
        return
    config = {}
    if os.path.exists(path):
        with open(path, "r") as f:
            config = json.load(f)
    config[key] = value
    with open(path, "w") as f:
        json.dump(config, f)
    await ctx.send(f'Konfiguration für \"{name}\" aktualisiert: {key} = {value}')

async def delete_tournament(ctx, name):
    import shutil
    guild_id = ctx.guild.id
    path = f'data/{guild_id}/{name}'
    if not os.path.exists(path):
        await ctx.send(f'❌ Turnier "{name}" existiert nicht!')
        return
    shutil.rmtree(path)
    await ctx.send(f'🗑️ Turnier "{name}" wurde gelöscht!')

async def unregister(ctx, tournament_name):
    guild_id = ctx.guild.id
    user_id = str(ctx.author.id)
    path = f'data/{guild_id}/{tournament_name}/players.json'
    if not os.path.exists(path):
        await ctx.send(f'Turnier \"{tournament_name}\" existiert nicht!')
        return
    players = []
    if os.path.exists(path):
        with open(path, "r") as f:
            players = json.load(f)
    if user_id not in players:
        await ctx.send("Du bist nicht registriert!")
        return
    players = [player for player in players if player["id"] != user_id]
    with open(path, "w") as f:
        json.dump(players, f)
    await ctx.send(f"{ctx.author.mention} wurde aus \"{tournament_name}\" entfernt!")

async def list_tournaments(ctx):
    guild_id = ctx.guild.id
    path = f'data/{guild_id}/'
    if not os.path.exists(path):
        await ctx.send("ℹ️ Keine Turniere gefunden!")
        return
    tournaments = []
    for d in os.listdir(path):
        config_path = os.path.join(path, d, "config.json")
        if os.path.isdir(os.path.join(path, d)) and os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)
            tournaments.append(f'**{config["name"]}** (Status: {config.get("status", "unbekannt")})')
    if not tournaments:
        await ctx.send("ℹ️ Keine Turniere gefunden!")
        return
    await ctx.send("**Aktive Turniere:**\n" + "\n".join(tournaments))

async def end_tournament(ctx, name):
    guild_id = ctx.guild.id
    config_path = f'data/{guild_id}/{name}/config.json'
    if not os.path.exists(config_path):
        await ctx.send(f'❌ Turnier "{name}" existiert nicht!')
        return
    with open(config_path, "r") as f:
        config = json.load(f)
    if config.get("status") == "ended":
        await ctx.send(f'⚠️ Turnier "{name}" ist bereits beendet!')
        return
    config["status"] = "ended"
    with open(config_path, "w") as f:
        json.dump(config, f)
    await ctx.send(f'🏁 Turnier "{name}" wurde beendet!')

async def reset_tournament(ctx, name):
    guild_id = ctx.guild.id
    path = f'data/{guild_id}/{name}/players.json'
    if os.path.exists(path):
        os.remove(path)
        await ctx.send(f'Teilnehmerliste für "{name}" wurde zurückgesetzt!')
    else:
        await ctx.send(f'Keine Teilnehmerliste für "{name}" gefunden!')

async def checkin(ctx, tournament_name):
    # Platzhalter für Check-In-Logik
    await ctx.send(f'Check-In für "{tournament_name}" gestartet!')

async def score(ctx, tournament_name, match_id, score1: int, score2: int):
    # Platzhalter für Score-Logik
    await ctx.send(f'Score für Match {match_id} in "{tournament_name}": {score1}:{score2} eingetragen!')

async def reopen_match(ctx, tournament_name, match_id):
    # Platzhalter für Reopen-Logik
    await ctx.send(f'Match {match_id} in "{tournament_name}" wurde wieder geöffnet!')

async def warn(ctx, tournament_name, match_id):
    # Platzhalter für Warn-Logik
    await ctx.send(f'Warnung für Match {match_id} in "{tournament_name}" gesendet!')

async def close_dispute(ctx, tournament_name, match_id):
    # Platzhalter für Dispute-Logik
    await ctx.send(f'Dispute für Match {match_id} in "{tournament_name}" geschlossen!')

async def template_create(ctx, name):
    await ctx.send(f"Template '{name}' erstellt (Platzhalter)!")

async def template_import(ctx, name):
    await ctx.send(f"Template '{name}' importiert (Platzhalter)!")

async def template_update(ctx, name):
    await ctx.send(f"Template '{name}' aktualisiert (Platzhalter)!")

async def template_delete(ctx, name):
    await ctx.send(f"Template '{name}' gelöscht (Platzhalter)!")

async def seeds(ctx, tournament_name):
    await ctx.send(f"Seeds für '{tournament_name}' anzeigen/bearbeiten (Platzhalter)!")

async def fake(ctx, tournament_name, count: int):
    guild_id = ctx.guild.id
    path = f'data/{guild_id}/{tournament_name}/players.json'
    if not os.path.exists(path):
        await ctx.send(f'Teilnehmerliste für "{tournament_name}" nicht gefunden!')
        return
    players = []
    if os.path.exists(path):
        with open(path, "r") as f:
            players = json.load(f)
    start_id = 100000000000000000  # Dummy-ID für Fake-Spieler
    for i in range(count):
        fake_id = f"fake_{start_id + len(players) + i}"
        players.append(fake_id)
    with open(path, "w") as f:
        json.dump(players, f)
    await ctx.send(f"{count} Fake-Spieler zu '{tournament_name}' hinzugefügt!")

async def rename(ctx, tournament_name, old_id: str, new_name: str):
    guild_id = ctx.guild.id
    path = f'data/{guild_id}/{tournament_name}/names.json'
    names = {}
    if os.path.exists(path):
        with open(path, "r") as f:
            names = json.load(f)
    names[old_id] = new_name
    with open(path, "w") as f:
        json.dump(names, f)
    await ctx.send(f"Spieler mit ID {old_id} wurde zu '{new_name}' umbenannt in '{tournament_name}'!")

async def kick(ctx, tournament_name, player_id: str):
    guild_id = ctx.guild.id
    path = f'data/{guild_id}/{tournament_name}/players.json'
    if not os.path.exists(path):
        await ctx.send(f'Teilnehmerliste für "{tournament_name}" nicht gefunden!')
        return
    with open(path, "r") as f:
        players = json.load(f)
    if player_id not in players:
        await ctx.send(f"Spieler mit ID {player_id} ist nicht registriert!")
        return
    players.remove(player_id)
    with open(path, "w") as f:
        json.dump(players, f)
    await ctx.send(f"Spieler mit ID {player_id} wurde aus '{tournament_name}' entfernt!")

async def unkick(ctx, tournament_name, player_id: str):
    guild_id = ctx.guild.id
    path = f'data/{guild_id}/{tournament_name}/players.json'
    if not os.path.exists(path):
        await ctx.send(f'Teilnehmerliste für "{tournament_name}" nicht gefunden!')
        return
    with open(path, "r") as f:
        players = json.load(f)
    if player_id in players:
        await ctx.send(f"Spieler mit ID {player_id} ist bereits registriert!")
        return
    players.append(player_id)
    with open(path, "w") as f:
        json.dump(players, f)
    await ctx.send(f"Spieler mit ID {player_id} wurde zu '{tournament_name}' hinzugefügt!")

async def team(ctx, tournament_name, team_name):
    await ctx.send(f"Team '{team_name}' in '{tournament_name}' bearbeitet (Platzhalter)!")

async def leave(ctx, tournament_name):
    await ctx.send(f"{ctx.author.mention} hat '{tournament_name}' verlassen (Platzhalter)!")

async def coinflip(ctx):
    import random
    result = random.choice(["Kopf", "Zahl"])
    await ctx.send(f"🪙 Münzwurf: {result}")

async def leaderboard_create(ctx, name):
    await ctx.send(f"Leaderboard '{name}' erstellt (Platzhalter)!")

async def leaderboard_config(ctx, name):
    await ctx.send(f"Leaderboard '{name}' konfiguriert (Platzhalter)!")

async def leaderboard_link(ctx, leaderboard_name, tournament_name):
    await ctx.send(f"Leaderboard '{leaderboard_name}' mit Turnier '{tournament_name}' verknüpft (Platzhalter)!")

async def leaderboard_move(ctx, leaderboard_name, channel: discord.TextChannel):
    await ctx.send(f"Leaderboard '{leaderboard_name}' in Kanal {channel.mention} verschoben (Platzhalter)!")

async def leaderboard_edit(ctx, leaderboard_name, player_name, points: int):
    await ctx.send(f"Spieler '{player_name}' in '{leaderboard_name}' auf {points} Punkte gesetzt (Platzhalter)!")

async def leaderboard_kick(ctx, leaderboard_name, player_name):
    await ctx.send(f"Spieler '{player_name}' aus '{leaderboard_name}' entfernt (Platzhalter)!")

async def leaderboard_ranking(ctx, leaderboard_name, points: int, role: discord.Role):
    await ctx.send(f"Rolle {role.mention} für {points} Punkte in '{leaderboard_name}' vergeben (Platzhalter)!")

async def leaderboard_export(ctx, leaderboard_name):
    await ctx.send(f"Leaderboard '{leaderboard_name}' als CSV exportiert (Platzhalter)!")

async def profile_region(ctx, region):
    await ctx.send(f"Region auf '{region}' gesetzt (Platzhalter)!")

async def profile_view(ctx):
    await ctx.send(f"Profil für {ctx.author.mention} anzeigen (Platzhalter)!")

async def admin_create(ctx, role: discord.Role):
    guild_id = ctx.guild.id
    path = f'data/{guild_id}/admin_role.json'
    with open(path, "w") as f:
        json.dump({"role_id": role.id}, f)
    await ctx.send(f"Admin-Rolle für Turniere ist jetzt: {role.mention}")

async def language(ctx, lang):
    guild_id = ctx.guild.id
    path = f'data/{guild_id}/language.json'
    with open(path, "w") as f:
        json.dump({"language": lang}, f)
    await ctx.send(f"Sprache für diesen Server gesetzt auf: {lang}")

async def branding(ctx, *, infos):
    guild_id = ctx.guild.id
    path = f'data/{guild_id}/branding.txt'
    with open(path, "w", encoding="utf-8") as f:
        f.write(infos)
    await ctx.send("Branding-Informationen gespeichert!")

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
        if rank not in allowed_ranks:
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

        # Teamnamen-Liste (du kannst beliebig erweitern)
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

    @bot.tree.command(name="start_ko_phase", description="Startet die K.O.-Phase mit den besten Teams aus jeder Gruppe")
    @app_commands.checks.has_permissions(administrator=True)
    async def start_ko_phase(interaction: discord.Interaction, tournament_name: str, teams_pro_gruppe: int = 2):
        guild_id = interaction.guild.id
        groups_path = f'data/{guild_id}/{tournament_name}/groups.json'
        matches_path = f'data/{guild_id}/{tournament_name}/group_matches.json'
        config_path = f'data/{guild_id}/{tournament_name}/config.json'
        if not os.path.exists(groups_path) or not os.path.exists(matches_path):
            await interaction.response.send_message("Gruppen oder Gruppenspiele nicht gefunden!", ephemeral=True)
            return

        with open(groups_path, "r") as f:
            groups = json.load(f)
        with open(matches_path, "r") as f:
            matches = json.load(f)
        with open(config_path, "r") as f:
            config = json.load(f)

        # Punkte für jedes Team berechnen
        team_points = {}
        for group_idx, group in enumerate(groups):
            for t_idx, team in enumerate(group):
                team_id = f"G{group_idx+1}_T{t_idx+1}"
                team_points[team_id] = 0

        # Team-IDs zuordnen
        team_lookup = {}
        for group_idx, group in enumerate(groups):
            for t_idx, team in enumerate(group):
                team_lookup[tuple(sorted([uid for uid, _ in team]))] = f"G{group_idx+1}_T{t_idx+1}"

        # Punkte aus Matches berechnen
        for match in matches:
            if match["score_a"] is not None and match["score_b"] is not None:
                team_a_id = team_lookup.get(tuple(sorted(match["team_a"])))
                team_b_id = team_lookup.get(tuple(sorted(match["team_b"])))
                if match["score_a"] > match["score_b"]:
                    team_points[team_a_id] += 3
                elif match["score_b"] > match["score_a"]:
                    team_points[team_b_id] += 3
                else:
                    team_points[team_a_id] += 1
                    team_points[team_b_id] += 1

        # Beste Teams pro Gruppe auswählen
        ko_teams = []
        for group_idx, group in enumerate(groups):
            group_team_ids = [f"G{group_idx+1}_T{t_idx+1}" for t_idx in range(len(group))]
            sorted_teams = sorted(group_team_ids, key=lambda tid: team_points[tid], reverse=True)
            ko_teams.extend(sorted_teams[:teams_pro_gruppe])

        # K.O.-Bracket erstellen (z.B. Viertelfinale)
        random.shuffle(ko_teams)
        ko_matches = []
        for i in range(0, len(ko_teams), 2):
            if i+1 < len(ko_teams):
                ko_matches.append({
                    "round": 1,
                    "team1": ko_teams[i],
                    "team2": ko_teams[i+1],
                    "score1": None,
                    "score2": None,
                    "winner": None
                })

        ko_path = f'data/{guild_id}/{tournament_name}/ko_bracket.json'
        with open(ko_path, "w") as f:
            json.dump(ko_matches, f, indent=2)

        # Phase auf KO setzen
        config["phase"] = "ko"
        with open(config_path, "w") as f:
            json.dump(config, f)

        await interaction.response.send_message(
            f"K.O.-Phase gestartet! {len(ko_teams)} Teams sind weiter. Die Paarungen wurden ausgelost und gespeichert.",
            ephemeral=False
        )

    @bot.tree.command(name="help", description="Zeigt alle Befehle und Hilfe an")
    async def help_command(interaction: discord.Interaction):
        help_text = (
            "**Tourney Bot Slash-Befehle:**\n"
            "/create_tournament – Turnier erstellen (Admin)\n"
            "/set_ranks – Ränge für Turnier setzen (Admin)\n"
            "/register – Für Turnier registrieren\n"
            "/shuffle_teams – Teams fair verteilen (Admin)\n"
            "/start_tournament – Turnier starten (Admin)\n"
            "/end_tournament – Turnier beenden (Admin)\n"
            "/list_tournaments – Zeigt alle Turniere\n"
            "/ping – Bot-Status\n"
            "/support – Support-Info\n"
            "/feedback – Feedback geben\n"
            "/invite – Bot einladen\n"
            "/premium – Infos zu Premium\n"
            # ...weitere Slash-Befehle hier ergänzen...
        )
        await interaction.response.send_message(help_text, ephemeral=True)

    @bot.tree.command(name="ping", description="Prüft, ob der Bot online ist")
    async def ping_command(interaction: discord.Interaction):
        await interaction.response.send_message("🏓 Pong! Der Bot ist online.", ephemeral=True)

    @bot.tree.command(name="support", description="Support-Info")
    async def support_command(interaction: discord.Interaction):
        await interaction.response.send_message("Support bekommst du hier: https://discord.gg/support-link", ephemeral=True)

    @bot.tree.command(name="feedback", description="Feedback geben")
    async def feedback_command(interaction: discord.Interaction):
        await interaction.response.send_message("Schreibe dein Feedback direkt hier in den Chat oder nutze unser Formular: https://example.com/feedback", ephemeral=True)

    @bot.tree.command(name="invite", description="Bot einladen")
    async def invite_command(interaction: discord.Interaction):
        await interaction.response.send_message("Lade den Bot ein: https://discord.com/oauth2/authorize?client_id=DEIN_BOT_ID&scope=bot&permissions=8", ephemeral=True)

    @bot.tree.command(name="premium", description="Infos zu Premium")
    async def premium_command(interaction: discord.Interaction):
        await interaction.response.send_message("Infos zu Premium findest du hier: https://example.com/premium", ephemeral=True)

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

    @bot.tree.command(name="kick", description="Entfernt einen Spieler aus einem Turnier")
    @app_commands.checks.has_permissions(administrator=True)
    async def kick(interaction: discord.Interaction, tournament_name: str, player_id: str):
        guild_id = interaction.guild.id
        path = f'data/{guild_id}/{tournament_name}/players.json'
        if not os.path.exists(path):
            await interaction.response.send_message(f'Teilnehmerliste für "{tournament_name}" nicht gefunden!', ephemeral=True)
            return
        with open(path, "r") as f:
            players = json.load(f)
        if player_id not in players:
            await interaction.response.send_message(f"Spieler mit ID {player_id} ist nicht registriert!", ephemeral=True)
            return
        players.pop(player_id)
        with open(path, "w") as f:
            json.dump(players, f)
        await interaction.response.send_message(f"Spieler mit ID {player_id} wurde aus '{tournament_name}' entfernt!", ephemeral=True)

    @bot.tree.command(name="rename", description="Benennt einen Spieler im Turnier um")
    @app_commands.checks.has_permissions(administrator=True)
    async def rename(interaction: discord.Interaction, tournament_name: str, player_id: str, new_name: str):
        guild_id = interaction.guild.id
        path = f'data/{guild_id}/{tournament_name}/names.json'
        names = {}
        if os.path.exists(path):
            with open(path, "r") as f:
                names = json.load(f)
        names[player_id] = new_name
        with open(path, "w") as f:
            json.dump(names, f)
        await interaction.response.send_message(f"Spieler mit ID {player_id} wurde zu '{new_name}' umbenannt in '{tournament_name}'!", ephemeral=True)

    @bot.tree.command(name="fake", description="Fügt Fake-Spieler zu einem Turnier hinzu")
    @app_commands.checks.has_permissions(administrator=True)
    async def fake(interaction: discord.Interaction, tournament_name: str, count: int):
        guild_id = interaction.guild.id
        path = f'data/{guild_id}/{tournament_name}/players.json'
        if not os.path.exists(path):
            await interaction.response.send_message(f'Teilnehmerliste für "{tournament_name}" nicht gefunden!', ephemeral=True)
            return
        players = {}
        if os.path.exists(path):
            with open(path, "r") as f:
                players = json.load(f)
        start_id = 100000000000000000  # Dummy-ID für Fake-Spieler
        for i in range(count):
            fake_id = f"fake_{start_id + len(players) + i}"
            players[fake_id] = {"ign": f"FakePlayer{len(players)+i+1}", "rank": "Unranked"}
        with open(path, "w") as f:
            json.dump(players, f)
        await interaction.response.send_message(f"{count} Fake-Spieler zu '{tournament_name}' hinzugefügt!", ephemeral=True)

    @bot.tree.command(name="checkin", description="Startet einen Check-In für ein Turnier")
    @app_commands.checks.has_permissions(administrator=True)
    async def checkin(interaction: discord.Interaction, tournament_name: str):
        await interaction.response.send_message(f'Check-In für "{tournament_name}" gestartet! (Platzhalter)', ephemeral=True)

    @bot.tree.command(name="score", description="Trage das Ergebnis eines Matches ein")
    @app_commands.checks.has_permissions(administrator=True)
    async def score(interaction: discord.Interaction, tournament_name: str, match_id: str, score1: int, score2: int):
        await interaction.response.send_message(f'Score für Match {match_id} in "{tournament_name}": {score1}:{score2} eingetragen! (Platzhalter)', ephemeral=True)

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

    @bot.tree.command(name="reopen_match", description="Öffnet ein Match erneut")
    @app_commands.checks.has_permissions(administrator=True)
    async def reopen_match(interaction: discord.Interaction, tournament_name: str, match_id: str):
        await interaction.response.send_message(f'Match {match_id} in "{tournament_name}" wurde wieder geöffnet! (Platzhalter)', ephemeral=True)

    @bot.tree.command(name="warn", description="Fordert ein Update für ein Match an")
    @app_commands.checks.has_permissions(administrator=True)
    async def warn(interaction: discord.Interaction, tournament_name: str, match_id: str):
        await interaction.response.send_message(f'Warnung für Match {match_id} in "{tournament_name}" gesendet! (Platzhalter)', ephemeral=True)

    @bot.tree.command(name="close_dispute", description="Schließt einen Dispute")
    @app_commands.checks.has_permissions(administrator=True)
    async def close_dispute(interaction: discord.Interaction, tournament_name: str, match_id: str):
        await interaction.response.send_message(f'Dispute für Match {match_id} in "{tournament_name}" geschlossen! (Platzhalter)', ephemeral=True)

    @bot.tree.command(name="template_create", description="Erstellt ein Turnier-Template")
    @app_commands.checks.has_permissions(administrator=True)
    async def template_create(interaction: discord.Interaction, name: str):
        await interaction.response.send_message(f"Template '{name}' erstellt! (Platzhalter)", ephemeral=True)

    @bot.tree.command(name="template_import", description="Importiert ein Turnier-Template")
    @app_commands.checks.has_permissions(administrator=True)
    async def template_import(interaction: discord.Interaction, name: str):
        await interaction.response.send_message(f"Template '{name}' importiert! (Platzhalter)", ephemeral=True)

    @bot.tree.command(name="template_update", description="Aktualisiert ein Turnier-Template")
    @app_commands.checks.has_permissions(administrator=True)
    async def template_update(interaction: discord.Interaction, name: str):
        await interaction.response.send_message(f"Template '{name}' aktualisiert! (Platzhalter)", ephemeral=True)

    @bot.tree.command(name="template_delete", description="Löscht ein Turnier-Template")
    @app_commands.checks.has_permissions(administrator=True)
    async def template_delete(interaction: discord.Interaction, name: str):
        await interaction.response.send_message(f"Template '{name}' gelöscht! (Platzhalter)", ephemeral=True)

    @bot.tree.command(name="seeds", description="Zeigt oder bearbeitet Seeds für ein Turnier")
    @app_commands.checks.has_permissions(administrator=True)
    async def seeds(interaction: discord.Interaction, tournament_name: str):
        await interaction.response.send_message(f"Seeds für '{tournament_name}' anzeigen/bearbeiten! (Platzhalter)", ephemeral=True)

    @bot.tree.command(name="unkick", description="Fügt einen Spieler wieder zu einem Turnier hinzu")
    @app_commands.checks.has_permissions(administrator=True)
    async def unkick(interaction: discord.Interaction, tournament_name: str, player_id: str):
        await interaction.response.send_message(f"Spieler mit ID {player_id} wurde zu '{tournament_name}' hinzugefügt! (Platzhalter)", ephemeral=True)

    @bot.tree.command(name="team", description="Bearbeitet ein Team in einem Turnier")
    @app_commands.checks.has_permissions(administrator=True)
    async def team(interaction: discord.Interaction, tournament_name: str, team_name: str):
        await interaction.response.send_message(f"Team '{team_name}' in '{tournament_name}' bearbeitet! (Platzhalter)", ephemeral=True)

    @bot.tree.command(name="leave", description="Verlasse ein Turnier")
    async def leave(interaction: discord.Interaction, tournament_name: str):
        await interaction.response.send_message(f"{interaction.user.mention} hat '{tournament_name}' verlassen! (Platzhalter)", ephemeral=True)

    @bot.tree.command(name="coinflip", description="Wirft eine Münze")
    async def coinflip(interaction: discord.Interaction):
        result = random.choice(["Kopf", "Zahl"])
        await interaction.response.send_message(f"🪙 Münzwurf: {result}", ephemeral=True)

    @bot.tree.command(name="leaderboard_create", description="Erstellt ein Leaderboard")
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

    @bot.tree.command(name="leaderboard_move", description="Verschiebt ein Leaderboard in einen anderen Kanal")
    @app_commands.checks.has_permissions(administrator=True)
    async def leaderboard_move(interaction: discord.Interaction, leaderboard_name: str, channel: discord.TextChannel):
        await interaction.response.send_message(f"Leaderboard '{leaderboard_name}' in Kanal {channel.mention} verschoben! (Platzhalter)", ephemeral=True)

    @bot.tree.command(name="leaderboard_edit", description="Bearbeitet die Punkte eines Spielers im Leaderboard")
    @app_commands.checks.has_permissions(administrator=True)
    async def leaderboard_edit(interaction: discord.Interaction, leaderboard_name: str, player_name: str, points: int):
        await interaction.response.send_message(f"Spieler '{player_name}' in '{leaderboard_name}' auf {points} Punkte gesetzt! (Platzhalter)", ephemeral=True)
    @bot.tree.command(name="profile_view", description="Zeigt dein Turnier-Profil an")
    async def profile_view(interaction: discord.Interaction):
        await interaction.response.send_message(f"Profil für {interaction.user.mention} anzeigen! (Platzhalter)", ephemeral=True)

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