import db

from collections import defaultdict



# -função get_tournament_teams()

def get_tournament_teams(tournament_id):

    return db.get_all_teams(tournament_id)

def get_team_players(team_id):

    return db.get_team_players(team_id)

def get_player_stats(player_id):

    return db.get_player_stats(player_id)

def get_player_best_map(player_id):

    stats = db.get_player_stats(player_id)

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


def get_avg_rating_map(player_id):

    stats = db.get_player_stats(player_id)

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
