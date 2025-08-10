
-- Sample Leagues
INSERT INTO league (league_id, name, country, tier_level) VALUES
(1, 'English Premier League', 'England', 1),
(2, 'Ligue 1', 'France', 1),
(3, 'Serie A', 'Italy', 1),
(4, 'Bundesliga', 'Germany', 1),
(5, 'La Liga', 'Spain', 1);

-- Sample Seasons
INSERT INTO season (season_id, league_id, year_start, year_end) VALUES
(1, 1, 2023, 2024),
(2, 2, 2023, 2024);

-- Sample Venues
INSERT INTO venue (venue_id, name, city, capacity) VALUES
(1, 'Old Trafford', 'Manchester', 74000),
(2, 'Parc des Princes', 'Paris', 48000);

-- Sample Teams
INSERT INTO team (team_id, name, home_venue_id, founded_year) VALUES
(1, 'Manchester United', 1, 1878),
(2, 'Paris Saint-Germain', 2, 1970);

-- Sample TeamSeason
INSERT INTO team_season (team_season_id, team_id, season_id, coach, final_position) VALUES
(1, 1, 1, 'Erik ten Hag', 3),
(2, 2, 2, 'Luis Enrique', 1);
