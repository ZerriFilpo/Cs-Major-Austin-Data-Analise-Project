import db

def main():
    # 0) Criar tabelas (se já existirem, o IF NOT EXISTS não quebra nada)
    db.create_tables()

    # 1) ROLES
    db.insert_role("rifler", "Rifler")
    db.insert_role("awper", "AWPer")
    db.insert_role("igl", "In-Game Leader")
    db.insert_role("coach", "Coach")

    # 2) TEAMS
    db.insert_team("FURIA", "FURIA Esports", "Brazil")
    db.insert_team("NAVI", "Natus Vincere", "Ukraine")

    # 3) COACHES
    db.insert_coach("guerri", "Nicholas Nogueira", "Brazil", "coach", "FURIA")
    db.insert_coach("b1ad3", "Andrii Gorodenskyi", "Ukraine", "coach", "NAVI")

    # 4) PLAYERS (10 jogadores, 5 pra cada time)
    # FURIA
    db.insert_player("KSCERATO", "Kaike Cerato", "Brazil", "rifler", "FURIA")
    db.insert_player("yuurih", "Yuri Santos", "Brazil", "rifler", "FURIA")
    db.insert_player("arT", "Andrei Piovezan", "Brazil", "igl", "FURIA")
    db.insert_player("chelo", "Marcelo Cespedes", "Brazil", "rifler", "FURIA")
    db.insert_player("fallen", "Gabriel Toledo", "Brazil", "awper", "FURIA")

    # NAVI
    db.insert_player("s1mple", "Oleksandr Kostyliev", "Ukraine", "awper", "NAVI")
    db.insert_player("b1t", "Valerii Vakhovskyi", "Ukraine", "rifler", "NAVI")
    db.insert_player("jL", "Justinas Lekavicius", "Lithuania", "rifler", "NAVI")
    db.insert_player("iM", "Ivan Mihai", "Romania", "rifler", "NAVI")
    db.insert_player("Aleksib", "Aleksi Virolainen", "Finland", "igl", "NAVI")

    # 5) MAPS
    db.insert_map("ancient", "Ancient")
    db.insert_map("mirage", "Mirage")

    # --- descobrir o id do s1mple pra usar como MVP e player_of_the_match ---
    conn = db.get_connection()
    cur = conn.execute("SELECT id FROM player WHERE nickname = ?", ("s1mple",))
    row = cur.fetchone()
    conn.close()

    if row is None:
        raise RuntimeError("Não encontrei o player s1mple no banco!")

    s1mple_id = row[0]

    # 6) TOURNAMENT
    db.insert_tournament(
        "BLAST_AUSTIN_2025",
        "BLAST.tv Austin Major 2025",
        "Austin, USA",
        "2025-05-10",
        "2025-05-24",
        s1mple_id,  # mvp_player_id
    )

    # 7) MATCHES – 1 partida (Grand Final)
    db.insert_match(
        "BLAST_AUSTIN_2025",  # tournament_id
        "Grand Final",        # round_des
        3,                    # best_of
        "FURIA",              # team1_id
        "NAVI",               # team2_id
        "NAVI",               # winner_team_id
        "2025-05-24",         # date
        s1mple_id,            # player_of_the_match
    )

    # Descobrir o id da match recém-criada
    conn = db.get_connection()
    cur = conn.execute("SELECT id FROM matches WHERE tournament_id = ? AND round_des = ?", ("BLAST_AUSTIN_2025", "Grand Final"))
    match_row = cur.fetchone()
    conn.close()

    if match_row is None:
        raise RuntimeError("Não encontrei a match Grand Final no banco!")

    match_id = match_row[0]

    # 8) MATCH_MAPS – 2 mapas (Ancient e Mirage)
    # Assumindo que a assinatura é:
    # insert_match_map(match_id, map_id, map_winner_team_id,
    #                  team1_ct_rounds, team1_ct_pistol,
    #                  team1_t_rounds, team1_t_pistol,
    #                  team2_ct_rounds, team2_ct_pistol,
    #                  team2_t_rounds, team2_t_pistol)

    # Ancient – NAVI ganha
    db.insert_match_map(
        match_id,
        "NAVI",
        5, 0,   # FURIA CT rounds/pistols
        7, 1,   # FURIA T rounds/pistols
        10, 1,  # NAVI CT rounds/pistols
        16, 1,  # NAVI T rounds/pistols
        "ancient",
    )

    # Mirage – NAVI ganha
    db.insert_match_map(
        match_id,
        "NAVI",
        4, 0,
        6, 1,
        11, 1,
        16, 1,
        "mirage",
    )

    # Descobrir ids dos match_map pra usar em player_map_stats
    conn = db.get_connection()
    cur = conn.execute("SELECT id, map_id FROM match_map WHERE match_id = ?", (match_id,))
    match_maps = cur.fetchall()
    conn.close()

    # Vamos mapear por mapa
    match_map_ids = {row[1]: row[0] for row in match_maps}
    ancient_mm_id = match_map_ids["ancient"]
    mirage_mm_id = match_map_ids["mirage"]

    # --- descobrir alguns player_id que vamos usar ---
    conn = db.get_connection()
    cur = conn.execute("SELECT id, nickname FROM player")
    players = cur.fetchall()
    conn.close()
    players_by_nick = {nick: pid for pid, nick in players}

    kscerato_id = players_by_nick["KSCERATO"]
    yuurih_id   = players_by_nick["yuurih"]
    b1t_id      = players_by_nick["b1t"]

    # 9) PLAYER_MAP_STATS – stats de alguns jogadores em Ancient e Mirage

    # Ancient – KSCERATO
    db.insert_player_map_stats(
        ancient_mm_id,
        kscerato_id,
        24,   # kills
        5,    # assists
        18,   # deaths
        78,   # kast
        85,   # dmr
    )

    # Ancient – b1t
    db.insert_player_map_stats(
        ancient_mm_id,
        b1t_id,
        20,
        3,
        17,
        74,
        88,
    )

    # Mirage – s1mple
    db.insert_player_map_stats(
        mirage_mm_id,
        s1mple_id,
        30,
        6,
        15,
        85,
        100,
    )

    # Mirage – yuurih
    db.insert_player_map_stats(
        mirage_mm_id,
        yuurih_id,
        19,
        4,
        21,
        69,
        82,
    )

    print("✅ Dados de teste inseridos com sucesso!")

    print(db.get_match_by_id(1))

if __name__ == "__main__":
    main()


