import pandas as pd
import os
import ssl
import urllib.request
from db import engine
from sqlalchemy import create_engine
from dotenv import load_dotenv


LEAGUE_CODES = {
    'E0': 'EPL',
    'D1': 'Bundesliga',
    'I1': 'Serie A',
    'F1': 'Ligue 1',
    'SP1': 'La Liga'
}

# Disable SSL verification for this download
ssl._create_default_https_context = ssl._create_unverified_context

def download_and_convert(league_code: str, season_code: str = '2223'):
    league_name = LEAGUE_CODES.get(league_code, league_code)
    url = f"https://www.football-data.co.uk/mmz4281/{season_code}/{league_code}.csv"

    print(f"📥 Downloading data from {url}")
    df = pd.read_csv(url)

    if 'Date' not in df.columns or 'HomeTeam' not in df.columns:
        print("❌ File format not compatible.")
        return

    df = df.rename(columns={
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
        'AR': 'away_red_cards',
    })

    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
    df['league'] = league_name
    df['season'] = '2022/2023'

    selected_columns = [
        'date', 'home_team', 'away_team', 'home_goals', 'away_goals',
        'home_shots', 'away_shots', 'home_shots_on_target', 'away_shots_on_target',
        'home_corners', 'away_corners', 'home_yellow_cards', 'away_yellow_cards',
        'home_red_cards', 'away_red_cards', 'league', 'season'
    ]

    df = df[[col for col in selected_columns if col in df.columns]]
    df.to_sql('staging_match_stats', engine, if_exists='append', index=False)
    print(f"✅ Loaded {len(df)} rows from {league_name} into staging_match_stats.")

if __name__ == '__main__':
    # Choose the leagues you want to load
    for code in ['E0', 'D1', 'I1', 'F1', 'SP1']:
        try:
            download_and_convert(code)
        except Exception as e:
            print(f"❌ Failed to load {code}: {e}")