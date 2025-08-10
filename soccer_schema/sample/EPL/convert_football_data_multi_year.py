import pandas as pd
import requests
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()  # Load .env with DB credentials

# Environment variables
DB_USERNAME = os.getenv("DB_USERNAME", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "soccer_db")

DATABASE_URL = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

LEAGUE_CODES = {
    'E0': 'EPL',
    'F1': 'Ligue 1',
    'I1': 'Serie A',
    'D1': 'Bundesliga',
    'SP1': 'La Liga'
}

YEARS = [(y, y + 1) for y in range(2022, 2025)]

def season_code(start, end):
    return f"{str(start)[-2:]}{str(end)[-2:]}"

def load_league_for_season(league_code, start_year, end_year):
    code = season_code(start_year, end_year)
    url = f"https://www.football-data.co.uk/mmz4281/{code}/{league_code}.csv"
    print(f"📥 Downloading {LEAGUE_CODES[league_code]} {start_year}/{end_year} from {url}")

    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        data = pd.read_csv(pd.compat.StringIO(response.text))
    except Exception as e:
        print(f"❌ Failed: {e}")
        return

    column_map = {
        'Date': 'date',
        'HomeTeam': 'home_team',
        'AwayTeam': 'away_team',
        'FTHG': 'home_goals',
        'FTAG': 'away_goals',
        'HS': 'home_shots',
        'AS': 'away_shots',
        'HST': 'home_shots_on_target',
        'AST': 'away_shots_on_target',
        'HC': 'home_corners',
        'AC': 'away_corners',
        'HY': 'home_yellow_cards',
        'AY': 'away_yellow_cards',
        'HR': 'home_red_cards',
        'AR': 'away_red_cards'
    }

    data = data.rename(columns=column_map)
    if 'date' not in data.columns:
        print("⚠️ No valid 'Date' column found.")
        return

    data['date'] = pd.to_datetime(data['date'], dayfirst=True, errors='coerce')
    data['league'] = LEAGUE_CODES[league_code]
    data['season'] = f"{start_year}/{end_year}"

    selected_cols = list(column_map.values()) + ['date', 'league', 'season']
    valid_cols = [c for c in selected_cols if c in data.columns]
    clean_data = data[valid_cols].dropna(subset=['date', 'home_team', 'away_team'])

    clean_data.to_sql("staging_match_stats", engine, if_exists="append", index=False)
    print(f"✅ Loaded {len(clean_data)} matches")

if __name__ == "__main__":
    for start_year, end_year in YEARS:
        for league_code in LEAGUE_CODES:
            load_league_for_season(league_code, start_year, end_year)
