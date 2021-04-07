

def Number_of_strikes_pitched(cursor,player_id):
	sql = '''select sum(total_s_counts) from GamePitcherStats where pitcher_id = {player_id};'''
	sql = sql.format(player_id = player_id)
	cursor.execute(sql)
	return cursor.fetchall()

def Number_of_strikeouts(cursor,player_id):
	sql = '''select count(*) from AtBats where pitcher_id = {player_id} and event = \'Strikeout\';'''
	sql = sql.format(player_id = player_id)
	cursor.execute(sql)
	return cursor.fetchall()

def Number_of_balls_pitched(cursor,player_id):
	sql = '''select sum(total_b_counts) from GamePitcherStats where pitcher_id = {player_id};'''
	sql = sql.format(player_id = player_id)
	cursor.execute(sql)
	return cursor.fetchall()

def Number_of_home_runs_allowed(cursor,player_id):
	sql = '''select count(*) from AtBats where pitcher_id = {player_id} and event = \'Home Run\';'''
	sql = sql.format(player_id = player_id)
	cursor.execute(sql)
	return cursor.fetchall()

def Total_pitches(cursor,player_id):
	sql = '''select sum(num_pitches) from GamePitcherStats where pitcher_id = {player_id};'''
	sql = sql.format(player_id = player_id)
	cursor.execute(sql)
	return cursor.fetchall()

def Average_spin_rate_and_direction(cursor,player_id):
	sql = '''select avg(avg_spin_rate), avg(avg_spin_dir) from GamePitcherStats where pitcher_id = {player_id};'''
	sql = sql.format(player_id = player_id)
	cursor.execute(sql)
	return cursor.fetchall()

def Average_pitch_speed(cursor,player_id):
	sql = '''select avg(avg_start_speed) from GamePitcherStats where pitcher_id = {player_id};'''
	sql = sql.format(player_id = player_id)
	cursor.execute(sql)
	return cursor.fetchall()

def Most_common_zone_pitched(cursor,player_id):
	sql = '''with A as (select most_common_zone, count(*) as pitches_in_zone from GamePitcherStats where pitcher_id = {player_id} group by most_common_zone)
select most_common_zone, pitches_in_zone from A where pitches_in_zone = (select max(pitches_in_zone) from A);'''
	sql = sql.format(player_id = player_id)
	cursor.execute(sql)
	return cursor.fetchall()

def Preferred_throwing_side(cursor,player_id):
	sql = '''with A as (select p_throws, count(*) as num_thrown_from_side from AtBats where pitcher_id = {player_id} group by p_throws)
select p_throws, num_thrown_from_side from A where num_thrown_from_side = (select max(num_thrown_from_side) from A);'''
	sql = sql.format(player_id = player_id)
	cursor.execute(sql)
	return cursor.fetchall()


def Most_common_pitch_type(cursor,player_id):
	sql = '''with A as (select pitch_type, count(*) as times_thrown from AtBats inner join Pitches on AtBats.ab_id = Pitches.ab_id where pitcher_id = {player_id} group by pitch_type)
select pitch_type, times_thrown from A where times_thrown = (select max(times_thrown) from A);'''
	sql = sql.format(player_id = player_id)
	cursor.execute(sql)
	return cursor.fetchall()

def consolidated_stats_pitcher(cursor,player_id):
	sql = '''select sum(total_s_counts), sum(total_b_counts), sum(num_pitches), avg(avg_spin_rate), avg(avg_spin_dir), avg(avg_start_speed)
    from GamePitcherStats where pitcher_id = {player_id};'''
    sql = sql.format(player_id = player_id)
	cursor.execute(sql)
	return cursor.fetchall()

def best_ptiche(cursor,player_id):
	sql = '''with A as (select pitcher_id, sum(num_pitches) as num_pitches from GamePitcherStats group by pitcher_id),
B as (select pitcher_id, count(*) as num_strikeouts from AtBats where event = \'Strikeout\' group by pitcher_id),
C as (select A.pitcher_id, B.num_strikeouts/A.num_pitches as ratio from A inner join B on A.pitcher_id = B.pitcher_id)
select pitcher_id, ratio from C where ratio = (select max(ratio) from C);'''
	sql = sql.format(player_id = player_id)
	cursor.execute(sql)
	return cursor.fetchall()

def Worst_pitcher(cursor,player_id):
	sql = '''with A as (select pitcher_id, sum(num_pitches) as num_pitches from GamePitcherStats group by pitcher_id),
B as (select pitcher_id, count(*) as num_strikeouts from AtBats where event = \'Strikeout\' group by pitcher_id),
C as (select A.pitcher_id, coalesce(B.num_strikeouts, 0)/A.num_pitches as ratio from A left join B on A.pitcher_id = B.pitcher_id)
select pitcher_id, ratio from C where ratio = (select min(ratio) from C);'''
	sql = sql.format(player_id = player_id)
	cursor.execute(sql)
	return cursor.fetchall()

