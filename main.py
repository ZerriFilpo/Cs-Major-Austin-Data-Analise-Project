import db

import stats_service as ss

print("Torunament teams")

print(ss.get_tournament_teams('BLAST_AUSTIN_2025'))

print("Team players")

print(ss.get_team_players('NAVI', 'BLAST_AUSTIN_2025'))

print("Player STAT")

print(ss.get_player_stats("PT001"))

print("player best map")

print(ss.get_player_best_map("PT001"))

print("PLAYER AVG RATING BY MAP")

print(ss.get_avg_rating_map("PT001"))

print("Scoreboard")

print(ss.get_scoreboard(1))

print("performance de maps")

print(ss.maps_performance_by_team("NAVI", "BLAST_AUSTIN_2025"))