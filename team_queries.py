def win_ratio_per_team(cursor):
	sql = '''WITH numWins AS ( SELECT count(*) as wins,team_id FROM GameTeamStats WHERE won = \'W\' GROUP BY team_id),
numGames AS ( SELECT count(*) as num_games, team_id FROM GameTeamStats GROUP BY team_id),
ratio AS ( SELECT wins/num_games AS win_ratio, numWins.team_id FROM numWins INNER JOIN numGames USING (team_id)),
ratioJoined AS ( SELECT win_ratio,team_name FROM ratio INNER JOIN Teams USING(team_id))
SELECT * FROM ratioJoined;'''
	cursor.execute(sql)
	return cursor.fetchall()

def best_win_ratio(cursor):
	sql = '''WITH numWins AS ( SELECT count(*) as wins,team_id FROM GameTeamStats WHERE won = \'W\' GROUP BY team_id),
numGames AS ( SELECT count(*) as num_games, team_id FROM GameTeamStats GROUP BY team_id),
ratio AS ( SELECT wins/num_games AS win_ratio, numWins.team_id FROM numWins INNER JOIN numGames USING (team_id)),
sorted AS ( SELECT * FROM ratio ORDER BY win_ratio DESC LIMIT 1),
ratioJoined AS ( SELECT win_ratio,team_name FROM sorted INNER JOIN Teams USING(team_id))
SELECT * FROM ratioJoined;'''
	cursor.execute(sql)
	return cursor.fetchall()

def win_ratio_vs_every_team(cursor,team):
	sql = '''WITH filterTeam AS (SELECT * FROM GameTeamStats WHERE team_id = \'{team}\'),
noFilterTeam AS ( SELECT * FROM GameTeamStats WHERE team_id != \'{team}\'),
meh AS (SELECT noFilterTeam.team_id, filterTeam.won FROM filterTeam INNER JOIN noFilterTeam USING (g_id)),
numGames AS ( SELECT COUNT(*) AS num_games,team_id FROM meh GROUP BY team_id),
numWon AS ( SELECT COUNT(*) AS num_won,team_id FROM meh WHERE won = \'W\' GROUP BY team_id),
merged AS ( SELECT num_won/num_games AS ratio, numGames.team_id FROM numGames INNER JOIN numWon USING (team_id)),
teamMerged AS ( SELECT ratio,team_name FROM merged LEFT JOIN Teams USING(team_id))
SELECT * FROM teamMerged;'''
	sql = sql.format(team=team)
	cursor.execute(sql)
	return cursor.fetchall()

def best_team_to_play_against(cusor,team):
	sql = '''WITH filterTeam AS (SELECT * FROM GameTeamStats WHERE team_id = \'{team}\'),
noFilterTeam AS ( SELECT * FROM GameTeamStats WHERE team_id != \'{team}\'),
meh AS (SELECT noFilterTeam.team_id, filterTeam.won FROM filterTeam INNER JOIN noFilterTeam USING (g_id)),
numGames AS ( SELECT COUNT(*) AS num_games,team_id FROM meh GROUP BY team_id),
numWon AS ( SELECT COUNT(*) AS num_won,team_id FROM meh WHERE won = \'W\' GROUP BY team_id),
merged AS ( SELECT num_won/num_games AS ratio, numGames.team_id FROM numGames INNER JOIN numWon USING (team_id)),
teamMerged AS ( SELECT ratio,team_name FROM merged LEFT JOIN Teams USING(team_id)),
bestTeam AS ( SELECT * FROM teamMerged ORDER BY ratio DESC LIMIT 1)
SELECT * FROM bestTeam;'''
	sql = sql.format(team=team)
	cursor.execute(sql)
	return cursor.fetchall()

def home_record_every_team(cursor):
	sql = '''WITH homeOnly AS ( SELECT * FROM GameTeamStats WHERE is_home_team = 1),
numGames AS ( SELECT COUNT(*) AS num_games, team_id FROM homeOnly GROUP BY team_id ),
homeWins AS ( SELECT COUNT(*) AS num_wins, team_id FROM homeOnly WHERE won = \'W\' GROUP BY team_id),
merged AS ( SELECT num_wins/num_games AS ratio, numGames.team_id FROM numGames INNER JOIN homeWins USING (team_id) ),
teamMerged AS ( SELECT ratio,team_name FROM merged LEFT JOIN Teams USING(team_id))
SELECT * FROM teamMerged;'''
	cursor.execute(sql)
	return cursor.fetchall()

def best_home_record(cursor):
	sql = '''WITH homeOnly AS ( SELECT * FROM GameTeamStats WHERE is_home_team = 1),
numGames AS ( SELECT COUNT(*) AS num_games, team_id FROM homeOnly GROUP BY team_id ),
homeWins AS ( SELECT COUNT(*) AS num_wins, team_id FROM homeOnly WHERE won = \'W\' GROUP BY team_id),
merged AS ( SELECT num_wins/num_games AS ratio, numGames.team_id FROM numGames INNER JOIN homeWins USING (team_id) ),
teamMerged AS ( SELECT ratio,team_name FROM merged LEFT JOIN Teams USING(team_id)),
bestTeam AS ( SELECT * FROM teamMerged ORDER BY ratio DESC LIMIT 1)
SELECT * FROM bestTeam;'''
	cursor.execute(sql)
	return cursor.fetchall()

def top_batters_in_terms_of_homeruns(cursor,team):
	sql = '''WITH hitsFilter AS ( SELECT batter_id, event, g_id FROM AtBats WHERE event = \'Home Run\' OR event = \'Single\' OR event = \'Double\' ),
teamFilter AS ( SELECT * FROM GameTeamStats WHERE team_id = \'{team}\'),
teamHits AS ( SELECT batter_id FROM teamFilter INNER JOIN hitsFilter USING (g_id)),
countHits AS ( SELECT COUNT(*) AS num_hits,batter_id FROM teamHits GROUP BY (batter_id) ),
numBatsSessions AS ( SELECT COUNT(*) AS num_sessions, batter_id FROM AtBats GROUP BY batter_id),
metricComplete AS ( SELECT num_hits/num_sessions AS hit_ratio,countHits.batter_id FROM countHits INNER JOIN numBatsSessions USING(batter_id)),
orderedHits AS ( SELECT * FROM metricComplete ORDER BY hit_ratio DESC LIMIT 5),
playerName AS ( SELECT CONCAT(first_name, \" \", last_name) AS name, hit_ratio FROM orderedHits LEFT JOIN Players ON orderedHits.batter_id = Players.player_id)
SELECT * FROM playerName;'''
	sql = sql.format(team=team)
	cursor.execute(sql)
	return cursor.fetchall()

def top_pitchers_in_terms_of_strikeout(cursor,team):
	sql = '''WITH pitchesFilter AS ( SELECT pitcher_id, event, g_id FROM AtBats WHERE event = \'Strikeout\' ),
teamFilter AS ( SELECT * FROM GameTeamStats WHERE team_id = \'{team}\'),
teampitches AS ( SELECT pitcher_id FROM teamFilter INNER JOIN pitchesFilter USING (g_id)),
countpitches AS ( SELECT COUNT(*) AS num_pitches,pitcher_id FROM teampitches GROUP BY (pitcher_id) ),
numBatsSessions AS ( select pitcher_id, sum(num_pitches) as num_sessions from GamePitcherStats group by pitcher_id),
metricComplete AS ( SELECT num_pitches/num_sessions AS pitcher_ratio,countpitches.pitcher_id FROM countpitches INNER JOIN numBatsSessions USING(pitcher_id)),
orderedpitches AS ( SELECT * FROM metricComplete ORDER BY pitcher_ratio DESC LIMIT 5),
playerName AS ( SELECT CONCAT(first_name, \" \", last_name) AS name, pitcher_ratio FROM orderedpitches LEFT JOIN Players ON orderedpitches.pitcher_id = Players.player_id)
SELECT * FROM playerName;'''
	sql = sql.format(team=team)
	cursor.execute(sql)
	return cursor.fetchall()


def most_player_apps(cursor,team):
	sql = '''WITH batters AS ( SELECT distinct g_id, batter_id FROM AtBats WHERE g_id IN (SELECT distinct g_id FROM GameTeamStats WHERE team_id = \'{team}\')),
pitchers AS ( SELECT distinct g_id,pitcher_id FROM AtBats WHERE g_id IN (SELECT distinct g_id FROM GameTeamStats WHERE team_id = \'{team}\')),
batterCount AS (SELECT COUNT(batter_id) AS batter_count, batter_id AS player_id FROM batters GROUP BY batter_id),
pitcherCount AS (SELECT COUNT(pitcher_id) AS pitcher_count, pitcher_id AS player_id FROM pitchers GROUP BY pitcher_id),
playerCount AS (SELECT player_id,(batter_count+pitcher_count) AS player_count FROM batterCount FULL JOIN  pitcherCount USING (player_id)),
topFive AS ( SELECT * FROM playerCount ORDER BY player_count DESC LIMIT 5),
playerName AS ( SELECT CONCAT(first_name, \" \", last_name) AS name, player_count FROM topFive LEFT JOIN Players ON topFive.player_id = Players.player_id)
SELECT * FROM playerName;'''
	sql = sql.format(team=team)
	cursor.execute(sql)
	return cursor.fetchall()