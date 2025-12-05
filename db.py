import sqlite3

from pathlib import Path

# Caminho para o arquivo do banco de dados (cs_major_stats.db)

BASE_DIR = Path(__file__).parent

DATABASE = BASE_DIR / "cs_major_stats.db"

# Função get_connection:

def get_connection():

    # - abre uma conexão com o arquivo cs_major_stats.db

    connection = sqlite3.connect(DATABASE)

    # - ativa o uso de foreign keys no SQLite

    connection.execute("PRAGMA foreign_keys = ON;")

    # - devolve essa conexão para ser usada em outras funções

    return connection

# Função create_tables:

def create_tables():
    
    # - abre uma conexão com o banco

    connection = get_connection()

    # - cria todas as tabelas necessárias (tournament, team, player, coach, map, matches, match_map, player_map_stats, role),

    # - cria tabela team

    connection.execute('''CREATE TABLE IF NOT EXISTS team(

    id TEXT PRIMARY KEY,
    
    name TEXT NOT NULL,

    country TEXT NOT NULL

    );''')

    # - cria tabela role

    connection.execute('''CREATE TABLE IF NOT EXISTS role(

    id TEXT PRIMARY KEY,

    name TEXT NOT NULL

    );''')

    # - cira tabela player

    connection.execute('''CREATE TABLE IF NOT EXISTS player(

    id INTEGER PRIMARY KEY,

    nickname TEXT NOT NULL,

    full_name TEXT NOT NULL,

    country TEXT NOT NULL

    );''')

    # - cria tabela tournament

    connection.execute('''CREATE TABLE IF NOT EXISTS tournament(

    id TEXT  PRIMARY KEY,
    
    name TEXT NOT NULL,

    location TEXT,
                       
    start_date TEXT,
                       
    end_date TEXT,

    mvp_player_id INTEGER REFERENCES player(id)

    );''')

    # - cria tabela player_tournament

    connection.execute('''CREATE TABLE IF NOT EXISTS player_tournament(

    id TEXT PRIMARY KEY,
                       
    player_id INTEGER REFERENCES player(id),
    
    tournament_id TEXT REFERENCES tournament(id),
    
    team_id TEXT REFERENCES team(id),
    
    role_id TEXT REFERENCES role(id)
    
    );''')

    # - cria tabela matches

    connection.execute('''CREATE TABLE IF NOT EXISTS matches(

    id INTEGER PRIMARY KEY,

    tournament_id TEXT REFERENCES tournament(id),

    round_des TEXT NOT NULL,

    best_of INTEGER NOT NULL,

    team1_id TEXT REFERENCES team(id),

    team2_id TEXT REFERENCES team(id),

    winner_team_id TEXT REFERENCES team(id),

    date TEXT NOT NULL,

    player_of_the_match INTEGER REFERENCES player_tournament(id)

    );''')

    # - cria tabela map

    connection.execute('''CREATE TABLE IF NOT EXISTS map(

    id TEXT PRIMARY KEY,

    name TEXT NOT NULL

    );''')

    # - cria tabela match_map

    connection.execute('''CREATE TABLE IF NOT EXISTS match_map(

    id INTEGER PRIMARY KEY,

    match_id INTEGER REFERENCES matches(id),

    map_winner TEXT REFERENCES team(id),

    team1_ct_rounds INTEGER NOT NULL,

    team1_ct_pistol INTEGER NOT NULL,

    team1_t_rounds INTEGER NOT NULL,

    team1_t_pistol INTEGER NOT NULL,

    team2_ct_rounds INTEGER NOT NULL,

    team2_ct_pistol INTEGER NOT NULL,   

    team2_t_rounds INTEGER NOT NULL,

    team2_t_pistol INTEGER NOT NULL,

    map_id TEXT REFERENCES map(id)

    );''')

    # - cira tabela player_map_stats

    connection.execute('''CREATE TABLE IF NOT EXISTS player_map_stats(

    id INTEGER PRIMARY KEY,

    match_map_id INTEGER REFERENCES match_map(id),

    player_id INTEGER REFERENCES player_tournament(id),

    kills INTEGER NOT NULL,

    assists INTEGER NOT NULL,

    deaths INTEGER NOT NULL,

    kast INTEGER NOT NULL,

    dmr INTEGER NOT NULL,

    rating REAL NOT NULL

    );''')

    # - faz commit

    connection.commit()

    # - fecha a conexão

    connection.close()

# Função insert_team(...) recebe dados do time (nome e região) e insere na tabela team

def insert_team(id, name, country):
    
    # - abre uma conexão com o banco

    connection = get_connection()

    # - insere dados na tabela

    connection.execute("INSERT INTO team (id, name, country) VALUES (?, ?, ?);", (id, name, country))

    # - faz commit

    connection.commit()

    # - fecha a conexão

    connection.close()

# Função insert_role(...) insere posições

def insert_role(id, name):
    
    # - abre uma conexão com o banco

    connection = get_connection()

    # - insere dados na tabela

    connection.execute("INSERT INTO role (id, name) VALUES (?, ?);", (id, name))

    # - faz commit

    connection.commit()

    # - fecha a conexão

    connection.close()

# Função insert_player(...) recebe  nickname, nome real, país, função, time e insere na tabela player

def insert_player(nickname, full_name, country):
    
    # - abre uma conexão com o banco

    connection = get_connection()

    # - insere dados na tabela

    connection.execute("INSERT INTO player (nickname, full_name, country) VALUES (?, ?, ?);", 
                       (nickname, full_name, country))

    # - faz commit

    connection.commit()

    # - fecha a conexão

    connection.close()

# Função insert_tournament(...) recebe dados do torneio e insere na tabela tournament

def insert_tournament(id, name, location, start_date, end_date, mvp_player_id):
    
    # - abre uma conexão com o banco

    connection = get_connection()

    # - insere dados na tabela

    connection.execute("INSERT INTO tournament (id, name, location, start_date, end_date, mvp_player_id) VALUES (?, ?, ?, ?, ?, ?);",
                        (id, name, location, start_date, end_date, mvp_player_id))

    # - faz commit

    connection.commit()

    # - fecha a conexão

    connection.close()


def insert_player_tournament(player_id, tournament_id, team_id, role_id):
    
    # - abre uma conexão com o banco

    connection = get_connection()

    # - insere dados na tabela

    connection.execute("INSERT INTO player_tournament (player_id, tournament_id, team_id, role_id) VALUES (?, ?, ?,?);", 
                       (player_id, tournament_id, team_id, role_id))

    # - faz commit

    connection.commit()

    # - fecha a conexão

    connection.close()

# Função insert_match(...) recebe times que disputaram a partida, tipo da partida, vencedor, resultado e insere em match

def insert_match(tournament_id, round_des, best_of, team1_id, team2_id, winner_team_id, date, player_of_the_match)  :
    
    # - abre uma conexão com o banco

    connection = get_connection()

    # - insere dados na tabela

    connection.execute("INSERT INTO matches (tournament_id, round_des, best_of, team1_id, team2_id, winner_team_id, date, player_of_the_match) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", 
                       (tournament_id, round_des, best_of, team1_id, team2_id, winner_team_id, date, player_of_the_match))

    # - faz commit

    connection.commit()

    # - fecha a conexão

    connection.close()

# Função insert_map(...) recebe nome do mapa e insere na tabela Maps   

def insert_map(id, name):
    
    # - abre uma conexão com o banco

    connection = get_connection()

    # - insere dados na tabela

    connection.execute("INSERT INTO map (id, name) VALUES (?, ?);", (id, name))

    # - faz commit

    connection.commit()

    # - fecha a conexão

    connection.close()

# Função insert_match_map(...) recebe dados de um mapa da série e insere em match_map

def insert_match_map(match_id, map_winner,team1_ct_rounds, team1_ct_pistol, team1_t_rounds, team1_t_pistol, 
                       team2_ct_rounds, team2_ct_pistol, team2_t_pistol, team2_t_rounds, map_id):
    
    # - abre uma conexão com o banco

    connection = get_connection()

    # - insere dados na tabela

    connection.execute("""INSERT INTO match_map (match_id, map_winner, team1_ct_rounds, team1_ct_pistol, team1_t_rounds, team1_t_pistol, 
                       team2_ct_rounds, team2_ct_pistol, team2_t_rounds, team2_t_pistol, map_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", 
                       (match_id, map_winner,team1_ct_rounds, team1_ct_pistol, team1_t_rounds, team1_t_pistol, team2_ct_rounds, team2_ct_pistol, team2_t_pistol, team2_t_rounds, map_id))

    # - faz commit

    connection.commit()

    # - fecha a conexão

    connection.close()

# Função insert_player_map_stats(...) recebe dados sobre o jogador (kills, deaths, assists, rating (kills/death), kast e dmr) em um mapa e insere em player_map_stats

def insert_player_map_stats(match_map_id, player_id, kills, assists, deaths, kast, dmr):
    
    # - abre uma conexão com o banco

    connection = get_connection()

    # - insere dados na tabela

    connection.execute("""INSERT INTO player_map_stats (match_map_id, player_id, kills, assists, deaths, kast, dmr, rating) VALUES (?, ?, ?, ?, ?, ?, ?, ?);""", 
                       (match_map_id, player_id, kills, assists, deaths, kast, dmr, round((kills/deaths), 2)))

    # - faz commit

    connection.commit()

    # - fecha a conexão

    connection.close()

# Função get_all_players() retorn lista de tuples[(id, Nome, Nome do time, Role)]

def get_all_players(tournament_id=None):

    # - abre uma conexão com o banco

    connection = get_connection()

    # Pegar players

    if(tournament_id is None):

        players = connection.execute("""SELECT
                                            p.id,
                                            
                                            p.nickname,
                                            
                                            p.country,
                                            
                                            t.name AS team_name,
                                            
                                            r.name AS role_name

                                        FROM player_tournament pt

                                        JOIN player p ON p.id = pt.player_id

                                        JOIN team t ON pt.team_id = t.id

                                        JOIN role r ON pt.role_id = r.id

                                        WHERE r.id <> 'coach'

                                        ORDER BY
                                            t.name, 
                                            
                                            CASE 
                                            
                                                WHEN r.id = "igl" THEN 0
                                                
                                                ELSE 1
                                            
                                            END,
                                            p.nickname;""")
        
    else:

        players = connection.execute("""SELECT
                                            p.id,
                                            
                                            p.nickname,
                                            
                                            p.country,
                                            
                                            t.name AS team_name,
                                            
                                            r.name AS role_name

                                        FROM player_tournament pt

                                        JOIN player p ON p.id = pt.player_id

                                        JOIN team t ON pt.team_id = t.id

                                        JOIN role r ON pt.role_id = r.id

                                        WHERE r.id <> 'coach' AND pt.tournament_id = ?

                                        ORDER BY
                                            t.name, 
                                            
                                            CASE 
                                            
                                                WHEN r.id = "igl" THEN 0
                                                
                                                ELSE 1
                                            
                                            END,
                                            p.nickname;""", (tournament_id,))

    rows = players.fetchall()

    # - fecha a conexão

    connection.close()

    return rows

def get_all_teams(tournament_id=None):

    # - abre uma conexão com o banco

    connection = get_connection()

    # Pegar teams

    if(tournament_id is None):

        teams = connection.execute("""SELECT team.* FROM team ORDER BY team.name;""")

    else:

        teams = connection.execute("""SELECT DISTINCT   
    
                                            t.*
                                            
                                        FROM matches m
                                        JOIN tournament tor ON tor.id = m.tournament_id
                                        JOIN team t ON t.id = m.team1_id OR t.id = m.team2_id
                                        WHERE tor.id = ?;""", (tournament_id,))

    rows = teams.fetchall()

    # - fecha a conexão

    connection.close()

    return rows

# função player por time get_team_players(team_id)

def get_team_players(team_id, tournament_id):

    # - abre uma conexão com o banco

    connection = get_connection()

    # pegar jogadores por team_id

    players = connection.execute("""SELECT

                                        p.nickname,
                                        
                                        r.name AS role_name,

                                        p.country
                                        
                                    FROM player_tournament pt

                                    JOIN player p ON p.id = pt.player_id

                                    JOIN role r ON pt.role_id = r.id

                                    WHERE pt.team_id = ? AND pt.tournament_id = ?

                                    ORDER BY 
                                        
                                        CASE
                                            
                                            WHEN r.id = 'igl' THEN 0
                                            ELSE 1
                                            
                                        END,
                                        
                                        p.nickname;""", (team_id, tournament_id))

    rows = players.fetchall()

    # - fecha a conexão

    connection.close()

    return rows

# função player por id get_player_by_id(player_id)

def get_player_by_id(player_id, tournament_id=None):

    # - abre uma conexão com o banco

    connection = get_connection()

    # pegar jogadores por team_id

    if tournament_id == None:

        player = connection.execute("""SELECT

                                            p.id,
                                            
                                            p.nickname,
                                            
                                            p.full_name,
                                            
                                            p.country

                                        FROM player p

                                        WHERE p.id = ?;""", (player_id,))

    else:

        player = connection.execute("""SELECT

                                            p.id,
                                            
                                            p.nickname,
                                            
                                            p.full_name,
                                            
                                            p.country,
                                            
                                            r.name AS role_name,
                                            
                                            t.name AS team_name
                                            

                                        FROM player_tournament pt

                                        JOIN player p ON p.id = pt.player_id

                                        JOIN role r ON pt.role_id = r.id

                                        JOIN team t ON pt.team_id = t.id

                                        WHERE p.id = ? AND pt.tournament_id = ?;""", (player_id, tournament_id))

    rows = player.fetchall()

    # - fecha a conexão

    connection.close()

    return rows

def get_player_stats(player_tournament_id):

    # - abre uma conexão com o banco

    connection = get_connection()

    # pegar jogadores por team_id

    player = connection.execute("""SELECT

                                        m.name AS map_name,
                                        
                                        tp.name AS player_team,
                                        
                                        top.name AS opponent_team,
                                        
                                        tw.name as winner_team,
                                        
                                        p.nickname,
                                        
                                        r.name,
                                        
                                        ps.kills,
                                        
                                        ps.assists,
                                        
                                        ps.deaths,
                                        
                                        ps.kast,
                                        
                                        ps.dmr,
                                        
                                        ps.rating
                                        
                                    FROM player_tournament pt, player_map_stats ps, match_map mm, matches mat

                                    JOIN player p ON p.id = pt.player_id

                                    JOIN team tp ON pt.team_id = tp.id

                                    JOIN team top ON (mat.team1_id = top.id AND mat.team1_id != pt.team_id AND mat.id = mm.match_id) OR 
                                    (mat.team2_id = top.id AND mat.team2_id != pt.team_id AND mat.id = mm.match_id)

                                    JOIN map m ON m.id = mm.map_id AND ps.match_map_id = mm.id

                                    JOIN team tw ON mat.winner_team_id = tw.id

                                    JOIN role r ON pt.role_id = r.id

                                    WHERE pt.id = ps.player_id
                                        AND pt.id = ?;""", (player_tournament_id,))

    rows = player.fetchall()

    # - fecha a conexão

    connection.close()

    return rows

# função get_match_by_id

def get_match_by_id(match_id):

    # - abre uma conexão com o banco

    connection = get_connection()

    # pegar jogadores por team_id

    player = connection.execute("""SELECT

                                        t1.name AS team1,
                                        
                                        t2.name AS team2,
                                        
                                        tw.name AS winner_team,

                                        m.round_des,

                                        m.best_of,
                                            
                                        m.date
                                        
                                    FROM matches m

                                    JOIN team t1 ON t1.id = m.team1_id

                                    JOIN team t2 ON t2.id = m.team2_id

                                    JOIN team tw ON tw.id = m.winner_team_id

                                    WHERE m.id = ?;""", (match_id,))

    rows = player.fetchall()

    # - fecha a conexão

    connection.close()

    return rows

# - função get_match_maps

def get_match_maps(match_id):

    # - abre uma conexão com o banco

    connection = get_connection()

    # - pegar lista de mapas

    maps = connection.execute("""SELECT
    
                                    tw.name,
                                    t1.name,
                                    mm.team1_ct_rounds,
                                    mm.team1_ct_pistol,
                                    mm.team1_t_rounds,
                                    mm.team1_t_pistol,
                                    t2.name,
                                    mm.team2_ct_rounds,
                                    mm.team2_ct_pistol,
                                    mm.team2_t_rounds,
                                    mm.team2_t_pistol,
                                    m.name

                                FROM match_map mm
                                JOIN matches mt ON mt.id = mm.match_id
                                JOIN map m ON m.id = mm.map_id
                                JOIN team tw ON tw.id = mm.map_winner
                                JOIN team t1 ON t1.id = mt.team1_id
                                JOIN team t2 ON t2.id = mt.team2_id
                                WHERE match_id = ?;""", (match_id,))

    rows = maps.fetchall()

    connection.close()

    return rows

def get_all_maps(tournament_id=None):

    # - abre uma conexão com o banco

    connection = get_connection()

    # Pegar maps
    if tournament_id == None:

        maps = connection.execute("""SELECT map.name FROM map;""")

    else:

        maps = connection.execute("""SELECT DISTINCT

                                            map.name

                                        FROM match_map mm

                                        JOIN map map ON map.id = mm.map_id

                                        JOIN matches m ON m.id = mm.match_id

                                        JOIN tournament t ON t.id = m.tournament_id

                                        WHERE t.id = ?;""", (tournament_id,))

    rows = maps.fetchall()

    # - fecha a conexão

    connection.close()

    return rows


    #existe tipo especifico para date no sql e outros tipos no slide 
    