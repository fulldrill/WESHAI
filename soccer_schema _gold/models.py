from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Time, Float
from db import Base

class League(Base):
    __tablename__ = 'league'
    league_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    tier_level = Column(Integer)

class Season(Base):
    __tablename__ = 'season'
    season_id = Column(Integer, primary_key=True)
    league_id = Column(Integer, ForeignKey('league.league_id'), nullable=False)
    year_start = Column(Integer, nullable=False)
    year_end = Column(Integer, nullable=False)

class Venue(Base):
    __tablename__ = 'venue'
    venue_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    city = Column(String)
    capacity = Column(Integer)

class Team(Base):
    __tablename__ = 'team'
    team_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    home_venue_id = Column(Integer, ForeignKey('venue.venue_id'))
    founded_year = Column(Integer)

class TeamSeason(Base):
    __tablename__ = 'team_season'
    team_season_id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('team.team_id'), nullable=False)
    season_id = Column(Integer, ForeignKey('season.season_id'), nullable=False)
    coach = Column(String)
    final_position = Column(Integer)

class Player(Base):
    __tablename__ = 'player'
    player_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    dob = Column(Date)
    nationality = Column(String)
    primary_position = Column(String)

class PlayerSeason(Base):
    __tablename__ = 'player_season'
    player_season_id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player.player_id'), nullable=False)
    team_season_id = Column(Integer, ForeignKey('team_season.team_season_id'), nullable=False)
    squad_number = Column(Integer)
    contract_start = Column(Date)
    contract_end = Column(Date)

class Referee(Base):
    __tablename__ = 'referee'
    referee_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    nationality = Column(String)

class EventType(Base):
    __tablename__ = 'event_type'
    event_type_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

class Match(Base):
    __tablename__ = 'match'
    match_id = Column(Integer, primary_key=True)
    season_id = Column(Integer, ForeignKey('season.season_id'), nullable=False)
    date = Column(Date, nullable=False)
    kick_off_time = Column(Time)
    venue_id = Column(Integer, ForeignKey('venue.venue_id'))
    referee_id = Column(Integer, ForeignKey('referee.referee_id'))

class MatchTeam(Base):
    __tablename__ = 'match_team'
    match_team_id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('match.match_id'), nullable=False)
    team_season_id = Column(Integer, ForeignKey('team_season.team_season_id'), nullable=False)
    is_home = Column(Boolean, nullable=False)
    goals_scored = Column(Integer)

class MatchEvent(Base):
    __tablename__ = 'match_event'
    event_id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('match.match_id'), nullable=False)
    event_type_id = Column(Integer, ForeignKey('event_type.event_type_id'), nullable=False)
    minute = Column(Integer)
    team_season_id = Column(Integer, ForeignKey('team_season.team_season_id'), nullable=False)
    player_id = Column(Integer, ForeignKey('player.player_id'))
    related_player_id = Column(Integer, ForeignKey('player.player_id'))

class TeamMatchStats(Base):
    __tablename__ = 'team_match_stats'
    tmstat_id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('match.match_id'), nullable=False)
    team_season_id = Column(Integer, ForeignKey('team_season.team_season_id'), nullable=False)
    possession_pct = Column(Float)
    shots = Column(Integer)
    shots_on_target = Column(Integer)
    corners = Column(Integer)
    fouls = Column(Integer)

class PlayerMatchStats(Base):
    __tablename__ = 'player_match_stats'
    pmstat_id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('match.match_id'), nullable=False)
    player_season_id = Column(Integer, ForeignKey('player_season.player_season_id'), nullable=False)
    minutes_played = Column(Integer)
    goals = Column(Integer)
    assists = Column(Integer)
    yellow_cards = Column(Integer)
    red_cards = Column(Integer)
