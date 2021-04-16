def avg_attendance_per_venue(cursor, venue_name):
	sql = '''WITH avgAtt AS (SELECT AVG(attendance) AS avg_attendance,venue_name FROM Games GROUP BY venue_name) 
SELECT avg_attendance FROM avgAtt WHERE venue_name = \'{venue_name}\';'''
	sql = sql.format(venue_name = venue_name)
	cursor.execute(sql)
	return cursor.fetchall()


def venue_with_most_average_attendance(cursor):
	sql = '''WITH AvgAttendance AS ( SELECT AVG(attendance) AS avg_attendance,venue_name FROM Games GROUP BY venue_name ),
MAxAvgAttendance AS (SELECT avg_attendance,venue_name FROM AvgAttendance ORDER BY avg_attendance DESC LIMIT 1)
SELECT CONCAT(venue_name, \" has the highest average attendance at \", avg_attendance) AS Answer FROM MAxAvgAttendance;'''
	cursor.execute(sql)
	return cursor.fetchall()


def best_game_attendance_per_venue(cursor, venue_name):
	sql = '''WITH MaxAttendancePerVenue AS ( SELECT max(attendance) AS attendance,venue_name FROM Games GROUP BY venue_name ),
MaxAttendanceGame AS ( SELECT home_team,away_team, Games.attendance , Games.venue_name FROM Games INNER JOIN MaxAttendancePerVenue using (attendance,venue_name)),
JoinHomeAttendance AS (SELECT MaxAttendanceGame.venue_name, MaxAttendanceGame.away_team, MaxAttendanceGame.attendance,Teams.team_name AS HOME_TEAM FROM MaxAttendanceGame INNER JOIN Teams ON MaxAttendanceGame.home_team = Teams.team_id),
JoinAwayAttendance AS (SELECT JoinHomeAttendance.venue_name,JoinHomeAttendance.HOME_TEAM, JoinHomeAttendance.attendance,Teams.team_name AS AWAY_TEAM FROM JoinHomeAttendance INNER JOIN Teams ON JoinHomeAttendance.away_team = Teams.team_id)
SELECT distinct CONCAT(HOME_TEAM, " vs ", AWAY_TEAM, " with attendance = ", attendance, " at ", venue_name) AS Answer FROM JoinAwayAttendance WHERE venue_name = \'{venue_name}\';'''
	sql = sql.format(venue_name = venue_name)
	cursor.execute(sql)
	return cursor.fetchall()


def best_attendance_ever(cursor):
	sql = '''WITH MaxAttendanceGame AS (SELECT home_team,away_team,attendance,venue_name FROM Games ORDER BY attendance DESC LIMIT 1),
JoinHomeAttendance AS (SELECT MaxAttendanceGame.venue_name, MaxAttendanceGame.away_team, MaxAttendanceGame.attendance,Teams.team_name AS HOME_TEAM FROM MaxAttendanceGame INNER JOIN Teams ON MaxAttendanceGame.home_team = Teams.team_id),
JoinAwayAttendance AS (SELECT JoinHomeAttendance.venue_name, JoinHomeAttendance.HOME_TEAM, JoinHomeAttendance.attendance,Teams.team_name AS AWAY_TEAM FROM JoinHomeAttendance INNER JOIN Teams ON JoinHomeAttendance.away_team = Teams.team_id)
SELECT CONCAT(HOME_TEAM, \" vs \", AWAY_TEAM, \" with an attendance of \", attendance, \" at \", venue_name) AS Answer FROM JoinAwayAttendance;'''
	cursor.execute(sql)
	return cursor.fetchall()


def most_games_played_at_venue(cursor):
	sql = '''WITH gamesPlayed AS ( SELECT count(venue_name) AS gameCount,venue_name FROM Games GROUP BY venue_name),
MaxGamesPlayed AS ( SELECT gameCount,venue_name FROM gamesPlayed ORDER BY gameCount DESC LIMIT 1)
SELECT CONCAT(venue_name, \" has hosted the most games with \", gameCount, " games played") AS Answer FROM MaxGamesPlayed;'''
	cursor.execute(sql)
	return cursor.fetchall()


def total_games_per_venue(cursor, venue_name):
	sql = '''SELECT CONCAT("Total of ", count(venue_name), " games played at ", venue_name) AS Answer FROM Games WHERE venue_name = \'{venue_name}\';'''
	sql = sql.format(venue_name = venue_name)
	cursor.execute(sql)
	return cursor.fetchall()


def average_score_per_venue(cursor, venue_name):
	sql = '''SELECT CONCAT(\"Average score at \", venue_name, \" is \" , avg(home_final_score + away_final_score)) AS Answer FROM Games WHERE venue_name = \'{venue_name}\';'''
	sql = sql.format(venue_name = venue_name)
	cursor.execute(sql)
	return cursor.fetchall()


def highest_average_across_all_venues(cursor):
	sql = '''WITH avgScore AS ( SELECT venue_name,avg(home_final_score + away_final_score) AS avg_score FROM Games GROUP BY venue_name ),
maxAvgScore AS ( SELECT * FROM avgScore ORDER BY avg_score DESC LIMIT 1)
SELECT CONCAT(\"Highest average score for any venue is at \", venue_name, \" with an average score of \" , avg_score) AS Answer FROM maxAvgScore;'''
	cursor.execute(sql)
	return cursor.fetchall()


def highest_scoring_game_for_venue(cursor, venue_name):
	sql = '''WITH maxScore AS ( SELECT max(home_final_score + away_final_score) AS max_score, venue_name  FROM Games GROUP BY venue_name),
maxScoreGames AS ( SELECT home_team,away_team,home_final_score,away_final_score,Games.venue_name FROM Games WHERE (home_final_score + away_final_score) = ( SELECT max_score FROM maxScore WHERE maxScore.venue_name = Games.venue_name)),
joinHomeTeam AS ( SELECT team_name AS HOME_TEAM ,away_team,home_final_score,away_final_score,venue_name FROM maxScoreGames LEFT JOIN Teams ON maxScoreGames.home_team = Teams.team_id ),
joinAwayTeam AS ( SELECT team_name AS AWAY_TEAM ,HOME_TEAM,home_final_score,away_final_score,venue_name FROM joinHomeTeam LEFT JOIN Teams ON joinHomeTeam.away_team = Teams.team_id )
SELECT CONCAT(venue_name, \" => \" , HOME_TEAM, \" vs \", AWAY_TEAM, \" => \", home_final_score, \" : \", away_final_score) AS Answer FROM joinAwayTeam WHERE venue_name = \'{venue_name}\';'''
	sql = sql.format(venue_name = venue_name)
	cursor.execute(sql)
	return cursor.fetchall()


def highest_scoring_games_across_all_venues(cursor):
	sql = '''WITH maxScore AS ( SELECT max(home_final_score + away_final_score) AS max_score, venue_name  FROM Games GROUP BY venue_name),
maxScoreGames AS ( SELECT home_team,away_team,home_final_score,away_final_score,Games.venue_name FROM Games WHERE (home_final_score + away_final_score) = ( SELECT max_score FROM maxScore WHERE maxScore.venue_name = Games.venue_name)),
joinHomeTeam AS ( SELECT team_name AS HOME_TEAM ,away_team,home_final_score,away_final_score,venue_name FROM maxScoreGames LEFT JOIN Teams ON maxScoreGames.home_team = Teams.team_id ),
joinAwayTeam AS ( SELECT team_name AS AWAY_TEAM ,HOME_TEAM,home_final_score,away_final_score,venue_name FROM joinHomeTeam LEFT JOIN Teams ON joinHomeTeam.away_team = Teams.team_id ),
maxOnly AS ( SELECT * FROM joinAwayTeam WHERE (home_final_score + away_final_score) = (SELECT max(home_final_score+away_final_score) FROM joinAwayTeam))
SELECT CONCAT(venue_name, \" => \" , HOME_TEAM, \" vs \", AWAY_TEAM, \" => \", home_final_score, \" : \", away_final_score) AS Answer FROM maxOnly ORDER BY venue_name;'''
	cursor.execute(sql)
	return cursor.fetchall()


def delay_games_per_venue(cursor, venue_name):
	sql = '''SELECT COUNT(*) AS tot_games_with_delay,venue_name FROM Games WHERE delay > 0 AND venue_name = \'{venue_name}\';'''
	sql = sql.format(venue_name = venue_name)
	cursor.execute(sql)
	return cursor.fetchall()


def most_delayed_games(cursor):
	sql = '''WITH delayCount AS ( SELECT count(*) AS delay_count,venue_name FROM Games WHERE delay > 0 GROUP BY venue_name ),
MAxdelayCount AS (SELECT delay_count,venue_name FROM delayCount ORDER BY delay_count DESC LIMIT 1)
SELECT CONCAT(venue_name, \" has had the most delayed games with \", delay_count) AS Answer FROM MAxdelayCount;'''
	cursor.execute(sql)
	return cursor.fetchall()


def avg_temp_per_venue(cursor, venue_name):
	sql = '''WITH tempExtracted AS ( SELECT venue_name, CAST(SUBSTRING(weather,1,LOCATE(' ',weather)-1) AS Signed) AS temp FROM Games)
SELECT AVG(temp) AS avg_temp FROM tempExtracted WHERE venue_name = \'{venue_name}\';'''
	sql = sql.format(venue_name = venue_name)
	cursor.execute(sql)
	return cursor.fetchall()
