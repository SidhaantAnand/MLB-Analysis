def consolidated_stats_pitcher(cursor, player_id):
	sql = '''select sum(total_s_counts), sum(total_b_counts), sum(num_pitches), avg(avg_spin_rate), avg(avg_spin_dir), avg(avg_start_speed)
	from GamePitcherStats where pitcher_id = {player_id};'''
	sql = sql.format(player_id = player_id)
	cursor.execute(sql)
	return cursor.fetchall()[0]


def Number_of_strikeouts(cursor, player_id):
	sql = '''select count(*) from AtBats where pitcher_id = {player_id} and event = \'Strikeout\';'''
	sql = sql.format(player_id = player_id)
	cursor.execute(sql)
	return cursor.fetchall()


def Number_of_home_runs_allowed(cursor, player_id):
	sql = '''select count(*) from AtBats where pitcher_id = {player_id} and event = \'Home Run\';'''
	sql = sql.format(player_id = player_id)
	cursor.execute(sql)
	return cursor.fetchall()


def Most_common_zone_pitched(cursor, player_id):
	sql = '''with A as (select most_common_zone, count(*) as pitches_in_zone from GamePitcherStats where pitcher_id = {player_id} group by most_common_zone)
select most_common_zone, pitches_in_zone from A where pitches_in_zone = (select max(pitches_in_zone) from A);'''
	sql = sql.format(player_id = player_id)
	cursor.execute(sql)
	return cursor.fetchall()


def Preferred_throwing_side(cursor, player_id):
	sql = '''with A as (select p_throws, count(*) as num_thrown_from_side from AtBats where pitcher_id = {player_id} group by p_throws)
	select p_throws, num_thrown_from_side from A where num_thrown_from_side = (select max(num_thrown_from_side) from A);'''
	sql = sql.format(player_id = player_id)
	cursor.execute(sql)
	return cursor.fetchall()


def Most_common_pitch_type(cursor, player_id):
	sql = '''with A as (select pitch_type, count(*) as times_thrown from AtBats inner join Pitches on AtBats.ab_id = Pitches.ab_id where pitcher_id = {player_id} group by pitch_type)
	select pitch_type, times_thrown from A where times_thrown = (select max(times_thrown) from A);'''
	sql = sql.format(player_id = player_id)
	cursor.execute(sql)
	return cursor.fetchall()


def best_pitcher(cursor):
	sql = '''with A as (select pitcher_id, sum(num_pitches) as num_pitches from GamePitcherStats group by pitcher_id),
	B as (select pitcher_id, count(*) as num_strikeouts from AtBats where event = \'Strikeout\' group by pitcher_id),
	C as (select A.pitcher_id, B.num_strikeouts/A.num_pitches as ratio from A inner join B on A.pitcher_id = B.pitcher_id),
	D as ( select pitcher_id, ratio from C ORDER BY ratio DESC  LIMIT 5)
	SELECT CONCAT(first_name, \" \", last_name) AS player_name, ratio FROM D LEFT JOIN Players ON D.pitcher_id = Players.player_id;;'''
	cursor.execute(sql)
	return cursor.fetchall()


def Worst_pitcher(cursor):
	sql = '''with A as (select pitcher_id, sum(num_pitches) as num_pitches from GamePitcherStats group by pitcher_id),
	B as (select pitcher_id, count(*) as num_strikeouts from AtBats where event = \'Strikeout\' group by pitcher_id),
	C as (select A.pitcher_id, coalesce(B.num_strikeouts, 0)/A.num_pitches as ratio from A left join B on A.pitcher_id = B.pitcher_id),
	D as ( select pitcher_id, ratio from C WHERE ratio != 0 AND ratio is NOT NULL ORDER BY ratio ASC  LIMIT 5)
	SELECT CONCAT(first_name, \" \", last_name) AS player_name, ratio FROM D LEFT JOIN Players ON D.pitcher_id = Players.player_id;;'''
	cursor.execute(sql)
	return cursor.fetchall()
