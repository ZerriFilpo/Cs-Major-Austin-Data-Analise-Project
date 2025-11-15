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

    # - cira tabela coach

    connection.execute('''CREATE TABLE IF NOT EXISTS coach(

    id INTEGER PRIMARY KEY,

    nickname TEXT NOT NULL,

    full_name TEXT NOT NULL,

    role_id TEXT REFERENCES role(id),

    team_id TEXT REFERENCES team(id)

    );''')

    # - cira tabela player

    connection.execute('''CREATE TABLE IF NOT EXISTS player(

    id INTEGER PRIMARY KEY,

    nickname TEXT NOT NULL,

    full_name TEXT NOT NULL,

    country TEXT NOT NULL,

    role_id TEXT REFERENCES role(id),

    team_id TEXT REFERENCES team(id)

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

    player_of_the_match INTEGER REFERENCES player(id)

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

    team2_t_pistol INTEGER NOT NULL,

    team2_t_rounds INTEGER NOT NULL,

    map_id TEXT REFERENCES map(id)

    );''')

    # - faz commit

    connection.commit()

    # - fecha a conexão

    connection.close()

# Função insert_tournament(...) recebe dados do torneio e insere na tabela tournament

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

# Função insert_player(...) recebe  nickname, nome real, país, função, time e insere na tabela player

# Função insert_coach(...) recebe  nickname, nome real, país, função, time e insere na tabela coach

# Função insert_map(...) recebe nome do mapa e insere na tabela Maps    

# Função insert_match(...) recebe times que disputaram a partida, tipo da partida, vencedor, resultado e insere em match

# Função insert_match_map(...) recebe dados de um mapa da série e insere em match_map

# Função player_map_stats(...) recebe dados sobre o jogador (kills, deaths, assists, rating (kills/death), kast e dmr) em um mapa e insere em player_map_stats

