import db

from collections import defaultdict



# -função get_tournament_teams()

def get_tournament_teams(tournament_id):

    return db.get_all_teams(tournament_id)

def get_team_players(team_id, tournament_id):

    return db.get_team_players(team_id, tournament_id)

def get_player_stats(player_tournament_id):

    return db.get_player_stats(player_tournament_id)

def get_player_best_map(player_tournament_id):

    stats = db.get_player_stats(player_tournament_id)

    if not stats:

        return 'N/A'

    agrupado = defaultdict(list)

    for row in stats:

        agrupado[row[0]].append(row[-1])

    avg_rating = 0

    for key, value in agrupado.items():
        
        avg = sum(value)/len(value)

        if avg > avg_rating:

            avg_rating = avg

            best_map = key

    return (best_map, avg_rating)


def get_avg_rating_map(player_tournament_id):

    stats = db.get_player_stats(player_tournament_id)

    if not stats:

        return 'N/A'

    agrupado = defaultdict(list)

    for row in stats:

        agrupado[row[0]].append(row[-1])

    medias = {}

    for key, value in agrupado.items():
        
        avg = sum(value)/len(value)

        medias[key] = value

    return medias

def get_scoreboard(match_id):

    maps = db.get_match_maps(match_id)

    match = db.get_match_by_id(match_id)[0]

    (t1, t2, tw, desc, bof, date) = match

    score = {"Match winner": tw}

    map_num = 1

    map_s = "map"

    winner = []

    for map in maps:
        
        (map_winner_team, map_t1, t1_ct_rounds,
        t1_ct_pistols, t1_t_rounds, t1_t_pistols, map_t2, 
        t2_ct_rounds, t2_ct_pistols, t2_t_rounds, t2_t_pistols,
        map_name) = map

        map_s1 = map_s + str(map_num)

        map_num += 1

        winner.append(map_winner_team)

        score[map_s1] = map_name

        score[map_s1 + "winner"] = map_winner_team

        total = t1_ct_rounds + t1_t_rounds

        score[map_s1 + " team1 rounds"] = total

        total = t2_ct_rounds + t2_t_rounds

        score[map_s1 + " team2 rounds"] = total

    score["Team1 maps"] = winner.count(t1)

    score["Team2 maps"] = winner.count(t2)

    return score

def maps_performance_by_team(team_id, tournament_id):

    connection = db.get_connection()

    all_maps = connection.execute("""SELECT

                                        mp.name,
                                        mm.map_winner

                                    FROM match_map mm
                                    JOIN map mp ON mp.id = mm.map_id
                                    JOIN matches m ON m.id = mm.match_id
                                    JOIN team t1 ON t1.id = m.team1_id
                                    JOIN team t2 ON t2.id = m.team2_id
                                    JOIN team tw ON tw.id = mm.map_winner
                                    WHERE m.team2_id = ? OR m.team1_id = ?
                                    AND m.tournament_id = ?;""", 
                        (team_id, team_id, tournament_id))

    victories = {}

    maps_played = {}

    maps = db.get_all_maps(tournament_id)

    for map in maps:

        victories[map[0]] = 0

        maps_played[map[0]] = 0
    
    for map in all_maps:

        (map_name, map_winner) = map

        if map_winner == team_id:

            victories[map_name] += 1
            
        maps_played[map_name] += 1

    maps_performance = {}

    for key, value in victories.items():

        win = value

        performance = round(win/maps_played[key], 2)

        maps_performance[key] = performance

    connection.close()

    return maps_performance 

def top_players(tournament_id):
    
    players = db.get_all_players(tournament_id)

    all_players_stats = {}

    for player in players:

        (id, nick, country, team, role) = player

        player_tournmanet_id = db.get_player_tournament_id(id, tournament_id)

        player_stats = db.get_player_stats(player_tournmanet_id)

        raiting = 0

        for stats in player_stats:

            raiting += stats[-1]

        if player_stats:

            raiting = raiting/len(player_stats)

            all_players_stats[player_tournmanet_id] = raiting

    s_all_players_stats = {k: v for k, v in sorted(all_players_stats.items(), key=lambda item: item[1], reverse=True)}

    return s_all_players_stats

def map_rate(tournament_id):

    all_maps = db.get_all_maps(tournament_id)

    all_matches = db.get_all_matches(tournament_id)

    resultado = {}

    for map in all_maps:

        resultado[map[0]] = []

    for match in all_matches:

        if resultado[match[0]]:

            new_ct = match[1] + match[3] + resultado[match[0]][0]

            new_t = match[2] + match[4] + resultado[match[0]][1]

            new_list = [new_ct, new_t]

            resultado[match[0]] = new_list
        
        else:

            new_ct = match[1] + match[3]

            new_t = match[2] + match[4]

            new_list = [new_ct, new_t]

            resultado[match[0]] = new_list

    for k, v in resultado.items():

        total_rounds = v[0] + v[1]

        ct_raiting = round(v[0]/total_rounds, 2)

        t_raiting = round(v[1]/total_rounds, 2)

        d = {"ct_raiting": ct_raiting, "t_raiting": t_raiting}

        resultado[k] = d

    return resultado

def team_pistol_rate(team_id, tournament_id):

    matches = db.all_team_matches(team_id, tournament_id)
    
    total_pistols = len(matches) * 2
    
    ct_pistols = 0

    t_pistols = 0

    for match in matches:

        (team1_id, team2_id, team1_ct, team1_t, team2_ct, team2_t) = match

        if team_id == team1_id:

            ct_pistols += team1_ct

            t_pistols += team1_t
        
        if team_id == team2_id:

            ct_pistols += team2_ct

            t_pistols += team2_t

    ct_rate = round(ct_pistols/total_pistols, 2)

    t_rate = round(t_pistols/total_pistols, 2)

    won_pistols = ct_pistols + t_pistols

    win_rate = round(won_pistols/total_pistols)

    ct_win_rate = round(ct_pistols/won_pistols, 2)

    t_win_rate = round(t_pistols/won_pistols, 2)

    resultado = {"CT rate": ct_rate, "T rate": t_rate, 
                 "Win rate": win_rate, "CT rate won pistols": ct_win_rate,
                 "T rate won pistols": t_win_rate}
    
    return resultado

def get_tournament():
    
    return db.get_all_tournament()