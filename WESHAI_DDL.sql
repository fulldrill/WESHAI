✅ Schema created in PostgreSQL

CREATE TABLE event_type (
        event_type_id SERIAL NOT NULL, 
        name VARCHAR NOT NULL, 
        description VARCHAR, 
        PRIMARY KEY (event_type_id)
)

;


CREATE TABLE league (
        league_id SERIAL NOT NULL, 
        name VARCHAR NOT NULL, 
        country VARCHAR NOT NULL, 
        tier_level INTEGER, 
        PRIMARY KEY (league_id)
)

;


CREATE TABLE player (
        player_id SERIAL NOT NULL, 
        first_name VARCHAR, 
        last_name VARCHAR, 
        dob DATE, 
        nationality VARCHAR, 
        primary_position VARCHAR, 
        PRIMARY KEY (player_id)
)

;


CREATE TABLE referee (
        referee_id SERIAL NOT NULL, 
        first_name VARCHAR, 
        last_name VARCHAR, 
        nationality VARCHAR, 
        PRIMARY KEY (referee_id)
)

;


CREATE TABLE venue (
        venue_id SERIAL NOT NULL, 
        name VARCHAR NOT NULL, 
        city VARCHAR, 
        capacity INTEGER, 
        PRIMARY KEY (venue_id)
)

;


CREATE TABLE season (
        season_id SERIAL NOT NULL, 
        league_id INTEGER NOT NULL, 
        year_start INTEGER NOT NULL, 
        year_end INTEGER NOT NULL, 
        PRIMARY KEY (season_id), 
        FOREIGN KEY(league_id) REFERENCES league (league_id)
)

;


CREATE TABLE team (
        team_id SERIAL NOT NULL, 
        name VARCHAR NOT NULL, 
        home_venue_id INTEGER, 
        founded_year INTEGER, 
        PRIMARY KEY (team_id), 
        FOREIGN KEY(home_venue_id) REFERENCES venue (venue_id)
)

;


CREATE TABLE match (
        match_id SERIAL NOT NULL, 
        season_id INTEGER NOT NULL, 
        date DATE NOT NULL, 
        kick_off_time TIME WITHOUT TIME ZONE, 
        venue_id INTEGER, 
        referee_id INTEGER, 
        PRIMARY KEY (match_id), 
        FOREIGN KEY(season_id) REFERENCES season (season_id), 
        FOREIGN KEY(venue_id) REFERENCES venue (venue_id), 
        FOREIGN KEY(referee_id) REFERENCES referee (referee_id)
)

;


CREATE TABLE team_season (
        team_season_id SERIAL NOT NULL, 
        team_id INTEGER NOT NULL, 
        season_id INTEGER NOT NULL, 
        coach VARCHAR, 
        final_position INTEGER, 
        PRIMARY KEY (team_season_id), 
        FOREIGN KEY(team_id) REFERENCES team (team_id), 
        FOREIGN KEY(season_id) REFERENCES season (season_id)
)

;


CREATE TABLE match_event (
        event_id SERIAL NOT NULL, 
        match_id INTEGER NOT NULL, 
        event_type_id INTEGER NOT NULL, 
        minute INTEGER, 
        team_season_id INTEGER NOT NULL, 
        player_id INTEGER, 
        related_player_id INTEGER, 
        PRIMARY KEY (event_id), 
        FOREIGN KEY(match_id) REFERENCES match (match_id), 
        FOREIGN KEY(event_type_id) REFERENCES event_type (event_type_id), 
        FOREIGN KEY(team_season_id) REFERENCES team_season (team_season_id), 
        FOREIGN KEY(player_id) REFERENCES player (player_id), 
        FOREIGN KEY(related_player_id) REFERENCES player (player_id)
)

;


CREATE TABLE match_team (
        match_team_id SERIAL NOT NULL, 
        match_id INTEGER NOT NULL, 
        team_season_id INTEGER NOT NULL, 
        is_home BOOLEAN NOT NULL, 
        goals_scored INTEGER, 
        PRIMARY KEY (match_team_id), 
        FOREIGN KEY(match_id) REFERENCES match (match_id), 
        FOREIGN KEY(team_season_id) REFERENCES team_season (team_season_id)
)

;


CREATE TABLE player_season (
        player_season_id SERIAL NOT NULL, 
        player_id INTEGER NOT NULL, 
        team_season_id INTEGER NOT NULL, 
        squad_number INTEGER, 
        contract_start DATE, 
        contract_end DATE, 
        PRIMARY KEY (player_season_id), 
        FOREIGN KEY(player_id) REFERENCES player (player_id), 
        FOREIGN KEY(team_season_id) REFERENCES team_season (team_season_id)
)

;


CREATE TABLE team_match_stats (
        tmstat_id SERIAL NOT NULL, 
        match_id INTEGER NOT NULL, 
        team_season_id INTEGER NOT NULL, 
        possession_pct FLOAT, 
        shots INTEGER, 
        shots_on_target INTEGER, 
        corners INTEGER, 
        fouls INTEGER, 
        PRIMARY KEY (tmstat_id), 
        FOREIGN KEY(match_id) REFERENCES match (match_id), 
        FOREIGN KEY(team_season_id) REFERENCES team_season (team_season_id)
)

;


CREATE TABLE player_match_stats (
        pmstat_id SERIAL NOT NULL, 
        match_id INTEGER NOT NULL, 
        player_season_id INTEGER NOT NULL, 
        minutes_played INTEGER, 
        goals INTEGER, 
        assists INTEGER, 
        yellow_cards INTEGER, 
        red_cards INTEGER, 
        PRIMARY KEY (pmstat_id), 
        FOREIGN KEY(match_id) REFERENCES match (match_id), 
        FOREIGN KEY(player_season_id) REFERENCES player_season (player_season_id)
)

;