import db
import sqlite3

def limpar_tabelas():
    """Apaga todos os dados (para o teste não dar conflito de PK)."""
    conn = db.get_connection()
    cur = conn.cursor()

    # Ordem respeitando FKs
    cur.execute("DELETE FROM player_map_stats;")
    cur.execute("DELETE FROM match_map;")
    cur.execute("DELETE FROM matches;")
    cur.execute("DELETE FROM player_tournament;")
    cur.execute("DELETE FROM tournament;")
    cur.execute("DELETE FROM map;")
    cur.execute("DELETE FROM team;")
    cur.execute("DELETE FROM role;")
    cur.execute("DELETE FROM player;")

    conn.commit()
    conn.close()


def main():
    # 0) Criar tabelas
    db.create_tables()

    # 1) Limpar tudo para o teste
    limpar_tabelas()

    # 2) ROLES
    db.insert_role("rifler", "Rifler")
    db.insert_role("awper", "AWPer")
    db.insert_role("igl", "In-Game Leader")
    db.insert_role("coach", "Coach")   # só como categoria extra

    # 3) TEAMS
    db.insert_team("FURIA", "FURIA Esports", "Brazil")
    db.insert_team("NAVI", "Natus Vincere", "Ukraine")

    # 4) PLAYERS (sem team nem role aqui)
    db.insert_player("KSCERATO", "Kaike Cerato", "Brazil")
    db.insert_player("yuurih",   "Yuri Santos", "Brazil")
    db.insert_player("arT",      "Andrei Piovezan", "Brazil")
    db.insert_player("chelo",    "Marcelo Cespedes", "Brazil")
    db.insert_player("fallen",   "Gabriel Toledo", "Brazil")

    db.insert_player("s1mple", "Oleksandr Kostyliev", "Ukraine")
    db.insert_player("b1t",    "Valerii Vakhovskyi", "Ukraine")
    db.insert_player("jL",     "Justinas Lekavicius", "Lithuania")
    db.insert_player("iM",     "Ivan Mihai", "Romania")
    db.insert_player("Aleksib","Aleksi Virolainen", "Finland")

    # 5) Buscar player_ids
    conn = db.get_connection()
    rows = conn.execute("SELECT id, nickname FROM player;").fetchall()
    conn.close()
    players = {nick: pid for (pid, nick) in rows}

    # 6) MAPAS
    db.insert_map("ancient", "Ancient")
    db.insert_map("mirage",  "Mirage")

    # 7) TOURNAMENT
    db.insert_tournament(
        "BLAST_AUSTIN_2025",
        "BLAST.tv Austin Major 2025",
        "Austin, USA",
        "2025-05-10",
        "2025-05-24",
        players["s1mple"],   # MVP é o s1mple (id de player)
    )

    # 8) PLAYER_TOURNAMENT (vamos inserir direto via SQL)
    #    Como teu schema usa id TEXT PRIMARY KEY, vamos inventar IDs tipo "PT001", "PT002", ...
    conn = db.get_connection()
    cur = conn.cursor()

    pt_ids = {}

    def add_pt(code, nick, team_id, role_id):
        player_id = players[nick]
        cur.execute("""
            INSERT INTO player_tournament (id, player_id, tournament_id, team_id, role_id)
            VALUES (?, ?, ?, ?, ?);
        """, (code, player_id, "BLAST_AUSTIN_2025", team_id, role_id))
        pt_ids[nick] = code

    # FURIA
    add_pt("PT001", "KSCERATO", "FURIA", "rifler")
    add_pt("PT002", "yuurih",   "FURIA", "rifler")
    add_pt("PT003", "arT",      "FURIA", "igl")
    add_pt("PT004", "chelo",    "FURIA", "rifler")
    add_pt("PT005", "fallen",   "FURIA", "awper")

    # NAVI
    add_pt("PT006", "s1mple", "NAVI", "awper")
    add_pt("PT007", "b1t",    "NAVI", "rifler")
    add_pt("PT008", "jL",     "NAVI", "rifler")
    add_pt("PT009", "iM",     "NAVI", "rifler")
    add_pt("PT010","Aleksib","NAVI", "igl")

    conn.commit()
    conn.close()

    # 9) MATCH (Grand Final)
    db.insert_match(
        "BLAST_AUSTIN_2025",  # tournament_id
        "Grand Final",        # round_des
        3,                    # best_of
        "FURIA",              # team1_id
        "NAVI",               # team2_id
        "NAVI",               # winner_team_id
        "2025-05-24",         # date
        pt_ids["s1mple"],     # player_of_the_match → player_tournament.id
    )

    # Descobrir id da match
    conn = db.get_connection()
    match_id = conn.execute(
        "SELECT id FROM matches WHERE tournament_id = ? AND round_des = ?;",
        ("BLAST_AUSTIN_2025", "Grand Final")
    ).fetchone()[0]
    conn.close()

    # 10) MATCH_MAPS – com pistols <= 2 por time no mapa

    # Ancient – NAVI vence 16–11
    # FURIA: 5 CT (0 pistols), 6 T (1 pistol) → 1 pistol no total
    # NAVI : 10 CT (1 pistol), 6 T (1 pistol) → 2 pistols (máximo)
    db.insert_match_map(
        match_id,
        "NAVI",   # map_winner
        5, 0,     # team1_ct_rounds, team1_ct_pistol
        6, 1,     # team1_t_rounds,  team1_t_pistol
        10, 1,    # team2_ct_rounds, team2_ct_pistol
        6, 1,     # team2_t_rounds,  team2_t_pistol
        "ancient"
    )

    # Mirage – NAVI vence 16–9
    # FURIA: 4 CT (0 pistols), 5 T (0 pistols) → 0 pistols
    # NAVI : 11 CT (1 pistol), 5 T (1 pistol) → 2 pistols
    db.insert_match_map(
        match_id,
        "NAVI",
        4, 0,
        5, 0,
        11, 1,
        5, 1,
        "mirage"
    )

    # Buscar ids dos match_map
    conn = db.get_connection()
    mm_rows = conn.execute(
        "SELECT id, map_id FROM match_map WHERE match_id = ?;",
        (match_id,)
    ).fetchall()
    conn.close()

    match_map_ids = {m_id: mm_id for (mm_id, m_id) in mm_rows}

    # 11) PLAYER_MAP_STATS – agora usando player_tournament.id (PT00x)
    db.insert_player_map_stats(
        match_map_ids["ancient"],
        pt_ids["KSCERATO"],
        24, 5, 18, 78, 85
    )

    db.insert_player_map_stats(
        match_map_ids["ancient"],
        pt_ids["b1t"],
        20, 3, 17, 74, 88
    )

    db.insert_player_map_stats(
        match_map_ids["mirage"],
        pt_ids["s1mple"],
        30, 6, 15, 85, 100
    )

    db.insert_player_map_stats(
        match_map_ids["mirage"],
        pt_ids["yuurih"],
        19, 4, 21, 69, 82
    )

    # 12) Alguns testes simples de leitura

    print("✅ Banco populado com sucesso!\n")

    print("📌 Match (get_match_by_id):")
    print(db.get_match_by_id(match_id))

    print("\n📌 Jogadores do torneio (get_all_players):")
    print(db.get_all_players("BLAST_AUSTIN_2025"))

    print("\n📌 Stats do s1mple (get_player_stats com player_tournament.id):")
    print(db.get_player_stats(pt_ids["s1mple"]))


if __name__ == "__main__":
    main()
