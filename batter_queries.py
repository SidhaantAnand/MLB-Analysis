# place holder values - should be set by the client application
player_name = "Matt Carpenter"
player_name_split = player_name.split()

# sql queries
# (num_ejections)
player_ejections_sql = f"""with playerId as
    (select player_id from Players where 
    first_name = '{player_name_split[0]}' and last_name = '{player_name_split[1]}')
    select count(*) as num_ejections from Ejections
    inner join AtBats using (ab_id)
    inner join playerId on AtBats.batter_id =  playerId.player_id;"""

# (num_times_out, num_hits, num_home_runs)
player_hits_outs_sql = f"""with playerId as
(select player_id from Players where 
first_name = '{player_name_split[0]}' and last_name = '{player_name_split[1]}')
select sum(outs) as num_outs, sum(hits) as num_hits, sum(home_runs) as num_home_runs from GameBatterStats
inner join playerId on playerId.player_id = GameBatterStats.batter_id
where batter_id = playerId.player_id;"""

# (most_played_inning, num_times_played_inning)
player_inning_sql = f"""with playerId as
    (select player_id from Players where 
    first_name = '{player_name_split[0]}' and last_name = '{player_name_split[1]}')
    select inning, count(inning) from AtBats
    inner join playerId on AtBats.batter_id =  playerId.player_id
    group by inning
    order by count(inning) desc
    limit 1;"""

# (prefered_side - L or R)
player_stand_sql = f"""with playerId as
    (select player_id from Players where 
    first_name = '{player_name_split[0]}' and last_name = '{player_name_split[1]}')
    select stand from AtBats
    inner join playerId on AtBats.batter_id =  playerId.player_id
    group by stand
    order by count(stand) desc
    limit 1;"""

# (best pitch type - w the least number of strikes)
player_best_pitch_type_sql = f"""with playerId as
    (select player_id from Players where 
    first_name = '{player_name_split[0]}' and last_name = '{player_name_split[1]}')
    select pitch_type from Pitches
    inner join AtBats on AtBats.ab_id = Pitches.ab_id
    inner join playerId on AtBats.batter_id =  playerId.player_id
    where code = 'B' or '*B'
    group by pitch_type
    order by count(pitch_type)/sum(b_count) desc
    limit 1;"""

# (worst pitch type - w the most number of strikes)
player_worst_pitch_type_sql = f"""with playerId as
    (select player_id from Players where 
    first_name = '{player_name_split[0]}' and last_name = '{player_name_split[1]}')
    select pitch_type from Pitches
    inner join AtBats on AtBats.ab_id = Pitches.ab_id
    inner join playerId on AtBats.batter_id =  playerId.player_id
    where code != 'B' and code != '*B'
    group by pitch_type
    order by count(pitch_type)/sum(b_count) desc
    limit 1;"""

# (best batter - balls:strikeout ratio)
best_batter_bsratio_sql = f"""with playerId as
    (select player_id, concat(first_name, ' ', last_name) as full_name from Players)
    select full_name from playerId
    inner join AtBats on AtBats.batter_id =  playerId.player_id
    inner join Pitches on AtBats.ab_id = Pitches.ab_id
    group by full_name
    order by sum(b_count)/sum(s_count) desc
    limit 1;"""

# (worst batter - balls:strikeout ratio)
worst_batter_bsratio_sql = f"""with playerId as
    (select player_id, concat(first_name, ' ', last_name) as full_name from Players)
    select full_name from playerId
    inner join AtBats on AtBats.batter_id =  playerId.player_id
    inner join Pitches on AtBats.ab_id = Pitches.ab_id
    group by full_name
    order by sum(b_count)/sum(s_count)
    limit 1;"""

# (best batter - hits:games ratio)
best_batter_hgratio_sql = f"""with playerId as
    (select player_id, concat(first_name, ' ', last_name) as full_name from Players)
    select full_name from playerId
    inner join GameBatterStats on GameBatterStats.batter_id =  playerId.player_id
    group by full_name
    order by sum(GameBatterStats.hits)/count(GameBatterStats.hits) desc
    limit 1;"""

# (worst batter - hits:games ratio)
worst_batter_hgratio_sql = f"""with playerId as
    (select player_id, concat(first_name, ' ', last_name) as full_name from Players)
    select full_name from playerId
    inner join GameBatterStats on GameBatterStats.batter_id =  playerId.player_id
    group by full_name
    order by sum(GameBatterStats.hits)/count(GameBatterStats.hits)
    limit 1;"""

# (best batter - home_runs:games ratio)
best_batter_hrgratio_sql = f"""with playerId as
    (select player_id, concat(first_name, ' ', last_name) as full_name from Players)
    select full_name from playerId
    inner join GameBatterStats on GameBatterStats.batter_id =  playerId.player_id
    group by full_name
    order by sum(GameBatterStats.home_runs)/count(GameBatterStats.home_runs) desc
    limit 1;"""

# (worst batter - home_runs:games ratio)
worst_batter_hrgratio_sql = f"""with playerId as
    (select player_id, concat(first_name, ' ', last_name) as full_name from Players)
    select full_name from playerId
    inner join GameBatterStats on GameBatterStats.batter_id =  playerId.player_id
    group by full_name
    order by sum(GameBatterStats.home_runs)/count(GameBatterStats.home_runs)
    limit 1;"""

# printing results - can print whatever query, more for the client side to handle
mycursor.execute(player_hits_outs_sql)
myresult = mycursor.fetchall()
for x in myresult:
    print(x)