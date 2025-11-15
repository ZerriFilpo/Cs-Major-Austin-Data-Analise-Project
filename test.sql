CREATE TABLE IF NOT EXISTS team(

    id TEXT PRIMARY KEY,
    
    name TEXT NOT NULL,

    country TEXT NOT NULL

    );

CREATE TABLE IF NOT EXISTS role(

    id TEXT PRIMARY KEY,

    name TEXT NOT NULL

    );

CREATE TABLE IF NOT EXISTS coach(

    id INTEGER PRIMARY KEY,

    nickname TEXT NOT NULL,

    full_name TEXT NOT NULL,

    role_id TEXT REFERENCES role(id),

    team_id TEXT REFERENCES team(id)

    );


CREATE TABLE IF NOT EXISTS player(

    id INTEGER PRIMARY KEY,

    nickname TEXT NOT NULL,

    full_name TEXT NOT NULL,

    country TEXT NOT NULL,

    role_id TEXT REFERENCES role(id),

    team_id TEXT REFERENCES team(id)

    );
    
CREATE TABLE IF NOT EXISTS tournament(

    id TEXT  PRIMARY KEY,
    
    name TEXT NOT NULL,

    location TEXT,
                       
    start_date TEXT,
                       
    end_date TEXT,

    mvp_player_id INTEGER REFERENCES player(id)

    );

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

CREATE TABLE IF NOT EXISTS map(

    id TEXT PRIMARY KEY,

    name TEXT NOT NULL

    );

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

