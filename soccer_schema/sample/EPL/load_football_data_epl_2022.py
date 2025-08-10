##Requirements
##Install pandas | pip install pandas

import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'soccer_db')

DATABASE_URL = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

CSV_URL = "https://www.football-data.co.uk/mmz4281/2223/E0.csv"

def load_epl_data_2022():
    df = pd.read_csv(CSV_URL)

    # Preview the file structure
    print("📊 Sample columns:", list(df.columns))

    # Filter required columns and rename them for your schema
    matches = df[[
        'Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'HS', 'AS', 'HST', 'AST',
        'HC', 'AC', 'HY', 'AY', 'HR', 'AR'
    ]].copy()

    # Convert date format
    matches['Date'] = pd.to_datetime(matches['Date'], dayfirst=True)
    
    # Map to your schema format
    matches_renamed = matches.rename(columns={
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
    })

    # Optionally assign league, season, match_id manually or via FK joins
    matches_renamed['season'] = '2022/2023'
    matches_renamed['league'] = 'EPL'

    # Insert into a staging table or directly into your match and team stats tables
    matches_renamed.to_sql('staging_match_stats', engine, if_exists='replace', index=False)
    print("✅ EPL 2022 match data loaded into 'staging_match_stats'")

if __name__ == '__main__':
    load_epl_data_2022()
