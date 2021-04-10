def highest_home_score(cursor):
	sql = '''
	WITH tmp AS ( select home_team, away_team, date, home_final_score, away_final_score from Games where home_final_score = (select max(home_final_score) from Games) ),
	homeJoined AS ( select team_name as home_team, away_team, date, home_final_score, away_final_score from tmp LEFT JOIN Teams ON tmp.home_team=Teams.team_id)
	SELECT home_team, team_name as away_team, date, home_final_score, away_final_score FROM homeJoined LEFT JOIN Teams ON homeJoined.away_team = Teams.team_id;
	
	'''
	cursor.execute(sql)
	return cursor.fetchall()

def higher_than_away_score(cursor):
	sql = '''
	WITH tmp AS ( select home_team, away_team, date, home_final_score, away_final_score from Games where away_final_score = (select max(away_final_score) from Games)),
	homeJoined AS ( select team_name as home_team, away_team, date, home_final_score, away_final_score from tmp LEFT JOIN Teams ON tmp.home_team=Teams.team_id)
	SELECT home_team, team_name as away_team, date, home_final_score, away_final_score FROM homeJoined LEFT JOIN Teams ON homeJoined.away_team = Teams.team_id;
	'''
	cursor.execute(sql)
	return cursor.fetchall()

def highest_combined_score(cursor):
	sql = '''
	WITH tmp AS ( select home_team, away_team, date, home_final_score, away_final_score from Games where (home_final_score + away_final_score = (select max(home_final_score + Games.away_final_score) from Games))),
	homeJoined AS ( select team_name as home_team, away_team, date, home_final_score, away_final_score from tmp LEFT JOIN Teams ON tmp.home_team=Teams.team_id)
	SELECT home_team, team_name as away_team, date, home_final_score, away_final_score FROM homeJoined LEFT JOIN Teams ON homeJoined.away_team = Teams.team_id;
	'''
	cursor.execute(sql)
	return cursor.fetchall()

def highest_attendance(cursor):
	sql = '''
	WITH tmp AS ( select home_team, away_team, date, attendance from Games where attendance = (select max(attendance) from Games) ),
	homeJoined AS ( select team_name as home_team, away_team, date, attendance  from tmp LEFT JOIN Teams ON tmp.home_team=Teams.team_id)
	SELECT home_team, team_name as away_team, date, attendance  FROM homeJoined LEFT JOIN Teams ON homeJoined.away_team = Teams.team_id;
	'''
	cursor.execute(sql)
	return cursor.fetchall()

def lowest_attendance(cursor):
	sql = '''
	WITH tmp AS ( select home_team, away_team, date, attendance from Games where attendance = (select min(attendance) from Games) ),
	homeJoined AS ( select team_name as home_team, away_team, date, attendance  from tmp LEFT JOIN Teams ON tmp.home_team=Teams.team_id)
	SELECT home_team, team_name as away_team, date, attendance  FROM homeJoined LEFT JOIN Teams ON homeJoined.away_team = Teams.team_id;
	'''
	cursor.execute(sql)
	return cursor.fetchall()

def higher_than_home_score_val(cursor,val):
	sql = '''select count(*) from Games where home_final_score > {val};'''
	sql = sql.format(val=val)
	cursor.execute(sql)
	return cursor.fetchall()

def higher_than_away_score_val(cursor,val):
	sql = '''select count(*) from Games where away_final_score > {val};'''
	sql = sql.format(val=val)
	cursor.execute(sql)
	return cursor.fetchall()

def Longest_game_elapsed_time(cursor):
	sql = '''select home_team, away_team, date, elapsed_time from Games where elapsed_time = (select max(elapsed_time) from Games);'''
	cursor.execute(sql)
	return cursor.fetchall()

def Longest_game_innings(cursor):
	sql = '''select distinct Games.g_id, inning from Games inner join AtBats on Games.g_id = AtBats.g_id where inning = (select max(inning) as highest_inning from AtBats);'''
	cursor.execute(sql)
	return cursor.fetchall()

def Shortest_game_elapsed_time(cursor):
	sql = '''select g_id, elapsed_time from Games where elapsed_time = (select min(elapsed_time) from Games);'''
	cursor.execute(sql)
	return cursor.fetchall()

def Longest_winning_streak(mydb,cursor):
	sql = '''set @seq:=0;'''
	cursor.execute(sql)
	mydb.commit()
	sql = '''with A as (select team_id, @seq:=if(won = \'W\', @seq + 1, 0) as win_streak from GameTeamStats order by team_id, g_id)
	select team_id, win_streak from A;'''
	cursor.execute(sql)
	return cursor.fetchall()

def Longest_losing_streak(mydb,cursor):
	sql = '''set @seq:=0;'''
	cursor.execute(sql)
	mydb.commit()
	sql = '''with A as (select team_id, @seq:=if(won = \'L\', @seq + 1, 0) as lose_streak from GameTeamStats order by team_id, g_id)
select team_id, lose_streak from A order by lose_streak desc limit 1;'''
	cursor.execute(sql)
	return cursor.fetchall()



