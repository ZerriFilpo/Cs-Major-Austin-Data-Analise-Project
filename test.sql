/* Criar team*/
CREATE TABLE IF NOT EXISTS team(

    id TEXT PRIMARY KEY,
    
    name TEXT NOT NULL,

    country TEXT NOT NULL

    );
    
/* Inserir times (CHECK)*/
INSERT INTO team (id, name, country) VALUES (?, ?, ?);

/* Criar role*/
CREATE TABLE IF NOT EXISTS role(

    id TEXT PRIMARY KEY,

    name TEXT NOT NULL

    );
    
/* Inserir roles (CHECK)*/
INSERT INTO role (id, name) VALUES (?, ?);

/* Criar coach*/
CREATE TABLE IF NOT EXISTS coach(

    id INTEGER PRIMARY KEY,

    nickname TEXT NOT NULL,

    full_name TEXT NOT NULL,
    
    country TEXT NOT NULL,

    role_id TEXT REFERENCES role(id),

    team_id TEXT REFERENCES team(id)

    );
    
/* Inserir coaches (CHECK)*/
INSERT INTO coach (nickname, full_name, country, role_id, team_id) VALUES (?, ?, ?, ?, ?);

/* Criar player*/
CREATE TABLE IF NOT EXISTS player(

    id INTEGER PRIMARY KEY,

    nickname TEXT NOT NULL,

    full_name TEXT NOT NULL,

    country TEXT NOT NULL,

    role_id TEXT REFERENCES role(id),

    team_id TEXT REFERENCES team(id)

    );

/* Inserir players (CHECK)*/
INSERT INTO player (nickname, full_name, country, role_id, team_id) VALUES (?, ?, ?, ?, ?, ?);
    
/* Criar tournament*/
CREATE TABLE IF NOT EXISTS tournament(

    id TEXT  PRIMARY KEY,
    
    name TEXT NOT NULL,

    location TEXT,
                       
    start_date TEXT,
                       
    end_date TEXT,

    mvp_player_id INTEGER REFERENCES player(id)

    );

/* Inserir tournament (CHECK)*/
INSERT INTO tournament (id, name, location, start_date, end_date, mvp_player_id) VALUES (?, ?, ?, ?, ?, ?);

/* Criar matches*/
CREATE TABLE IF NOT EXISTS matches(

    id INTEGER PRIMARY KEY,

    tournament_id TEXT REFERENCES tournament(id),

    round_des TEXT NOT NULL,

    best_of INTEGER NOT NULL,

    team1_id TEXT REFERENCES team(id),

    team2_id TEXT REFERENCES team(id),

    winner_team_id TEXT REFERENCES team(id),

    date TEXT NOT NULL,

    player_of_the_match INTEGER REFERENCES player(id)

    );

/* Inserir matches (CHECK)*/
INSERT INTO matches (tournament_id, round_des, best_of, team1_id, team2_id, winner_team_id, date, player_of_the_match) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    
/* Criar map*/
CREATE TABLE IF NOT EXISTS map(

    id TEXT PRIMARY KEY,

    name TEXT NOT NULL

    );

/* Inserir map (CHECK)*/
INSERT INTO map (id, name) VALUES (?, ?);

/* Criar match_map*/
CREATE TABLE IF NOT EXISTS match_map(

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

    );

/* Inserir match_map (CHECK)*/
INSERT INTO match_map (match_id, map_winner,team1_ct_rounds, team1_ct_pistol, team1_t_rounds, team1_t_pistol, team2_ct_rounds, team2_ct_pistol, team2_t_pistol, team2_t_rounds, map_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);


/* Criar player_map_stats*/
CREATE TABLE IF NOT EXISTS player_map_stats(

    id INTEGER PRIMARY KEY,

    match_map_id INTEGER REFERENCES match_map(id),

    player_id INTEGER REFERENCES player(id),

    kills INTEGER NOT NULL,

    assists INTEGER NOT NULL,

    deaths INTEGER NOT NULL,

    kast INTEGER NOT NULL,

    dmr INTEGER NOT,

    rating REAL NOT NULL

    );

/* Inserir player_map_stats (CHECK)*/
INSERT INTO player_map_stats (match_map_id, player_id, kills, assists, deaths, KAST, dmr, rating) VALUES (?, ?, ?, ?, ?, ?, ?, ?);