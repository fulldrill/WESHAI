import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'soccer_db')

DATABASE_URL = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

def export_match_data(year):
    query = f"""
    SELECT m.match_id, m.date, l.name AS league, s.year_start, s.year_end,
           ht.name AS home_team, at.name AS away_team, 
           mt_home.goals_scored AS home_goals, mt_away.goals_scored AS away_goals
    FROM match m
    JOIN season s ON m.season_id = s.season_id
    JOIN league l ON s.league_id = l.league_id
    JOIN match_team mt_home ON m.match_id = mt_home.match_id AND mt_home.is_home = TRUE
    JOIN match_team mt_away ON m.match_id = mt_away.match_id AND mt_away.is_home = FALSE
    JOIN team_season ts_home ON mt_home.team_season_id = ts_home.team_season_id
    JOIN team_season ts_away ON mt_away.team_season_id = ts_away.team_season_id
    JOIN team ht ON ts_home.team_id = ht.team_id
    JOIN team at ON ts_away.team_id = at.team_id
    WHERE s.year_start = {year}
    ORDER BY m.date;
    """
    df = pd.read_sql(query, engine)
    df.to_csv(f"matches_{year}.csv", index=False)
    print(f"✅ Match data exported for {year}")

def export_player_stats(year):
    query = f"""
    SELECT p.first_name || ' ' || p.last_name AS player, psn.squad_number, t.name AS team, 
           l.name AS league, s.year_start, s.year_end,
           pms.match_id, pms.minutes_played, pms.goals, pms.assists, 
           pms.yellow_cards, pms.red_cards
    FROM player_match_stats pms
    JOIN player_season psn ON pms.player_season_id = psn.player_season_id
    JOIN player p ON psn.player_id = p.player_id
    JOIN team_season ts ON psn.team_season_id = ts.team_season_id
    JOIN team t ON ts.team_id = t.team_id
    JOIN season s ON ts.season_id = s.season_id
    JOIN league l ON s.league_id = l.league_id
    WHERE s.year_start = {year};
    """
    df = pd.read_sql(query, engine)
    df.to_csv(f"player_stats_{year}.csv", index=False)
    print(f"✅ Player stats exported for {year}")

def export_team_stats(year):
    query = f"""
    SELECT t.name AS team, l.name AS league, s.year_start, s.year_end,
           tms.match_id, tms.possession_pct, tms.shots, tms.shots_on_target, 
           tms.corners, tms.fouls
    FROM team_match_stats tms
    JOIN team_season ts ON tms.team_season_id = ts.team_season_id
    JOIN team t ON ts.team_id = t.team_id
    JOIN season s ON ts.season_id = s.season_id
    JOIN league l ON s.league_id = l.league_id
    WHERE s.year_start = {year};
    """
    df = pd.read_sql(query, engine)
    df.to_csv(f"team_stats_{year}.csv", index=False)
    print(f"✅ Team stats exported for {year}")

if __name__ == '__main__':
    years = [2022, 2023, 2024]  # Add or adjust years as needed
    for y in years:
        export_match_data(y)
        export_player_stats(y)
        export_team_stats(y)
