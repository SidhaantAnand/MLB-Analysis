# (num_ejections)
def player_ejections(mycursor, player_name):
    player_name_split = player_name.split()
    sql = f"""with playerId as
        (select player_id from Players where 
        first_name = '{player_name_split[0]}' and last_name = '{player_name_split[1]}')
        select count(*) as num_ejections from Ejections
        inner join AtBats using (ab_id)
        inner join playerId on AtBats.batter_id =  playerId.player_id;"""
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

# (num_times_out, num_hits, num_home_runs)
def player_hits_outs(mycursor, player_name):
    player_name_split = player_name.split()
    sql = f"""with playerId as
        (select player_id from Players where 
        first_name = '{player_name_split[0]}' and last_name = '{player_name_split[1]}')
        select sum(outs) as num_outs, sum(hits) as num_hits, sum(home_runs) as num_home_runs from GameBatterStats
        inner join playerId on playerId.player_id = GameBatterStats.batter_id
        where batter_id = playerId.player_id;"""
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

# (most_played_inning, num_times_played_inning)
def player_inning(mycursor, player_name):
    player_name_split = player_name.split()
    sql = f"""with playerId as
        (select player_id from Players where 
        first_name = '{player_name_split[0]}' and last_name = '{player_name_split[1]}')
        select inning, count(inning) from AtBats
        inner join playerId on AtBats.batter_id =  playerId.player_id
        group by inning
        order by count(inning) desc
        limit 1;"""
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

# (prefered_side - L or R)
def player_stand(mycursor, player_name):
    player_name_split = player_name.split()
    sql = f"""with playerId as
        (select player_id from Players where 
        first_name = '{player_name_split[0]}' and last_name = '{player_name_split[1]}')
        select stand from AtBats
        inner join playerId on AtBats.batter_id =  playerId.player_id
        group by stand
        order by count(stand) desc
        limit 1;"""
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

# (best pitch type - w the least number of strikes)
def player_best_pitch_type(mycursor, player_name):
    player_name_split = player_name.split()
    sql = f"""with playerId as
        (select player_id from Players where 
        first_name = '{player_name_split[0]}' and last_name = '{player_name_split[1]}')
        select pitch_type from Pitches
        inner join AtBats on AtBats.ab_id = Pitches.ab_id
        inner join playerId on AtBats.batter_id =  playerId.player_id
        where code = 'B' or '*B'
        group by pitch_type
        order by count(pitch_type)/sum(b_count) desc
        limit 1;"""
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

# (worst pitch type - w the most number of strikes)
def player_worst_pitch_type(mycursor, player_name):
    player_name_split = player_name.split()
    sql = f"""with playerId as
        (select player_id from Players where 
        first_name = '{player_name_split[0]}' and last_name = '{player_name_split[1]}')
        select pitch_type from Pitches
        inner join AtBats on AtBats.ab_id = Pitches.ab_id
        inner join playerId on AtBats.batter_id =  playerId.player_id
        where code != 'B' and code != '*B'
        group by pitch_type
        order by count(pitch_type)/sum(b_count) desc
        limit 1;"""
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

# (best batter - balls:strikeout ratio)
def best_batter_bsratio(mycursor):
    sql = f"""with playerId as
        (select player_id, concat(first_name, ' ', last_name) as full_name from Players)
        select full_name from playerId
        inner join AtBats on AtBats.batter_id =  playerId.player_id
        inner join Pitches on AtBats.ab_id = Pitches.ab_id
        group by full_name
        order by sum(b_count)/sum(s_count) desc
        limit 1;"""
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

# (worst batter - balls:strikeout ratio)
def worst_batter_bsratio(mycursor):
    sql = f"""with playerId as
        (select player_id, concat(first_name, ' ', last_name) as full_name from Players)
        select full_name from playerId
        inner join AtBats on AtBats.batter_id =  playerId.player_id
        inner join Pitches on AtBats.ab_id = Pitches.ab_id
        group by full_name
        order by sum(b_count)/sum(s_count)
        limit 1;"""
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

# (best batter - hits:games ratio)
def best_batter_hgratio(mycursor):
    sql = f"""with playerId as
        (select player_id, concat(first_name, ' ', last_name) as full_name from Players)
        select full_name from playerId
        inner join GameBatterStats on GameBatterStats.batter_id =  playerId.player_id
        group by full_name
        order by sum(GameBatterStats.hits)/count(GameBatterStats.hits) desc
        limit 1;"""
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

# (worst batter - hits:games ratio)
def worst_batter_hgratio(mycursor):
    sql = f"""with playerId as
        (select player_id, concat(first_name, ' ', last_name) as full_name from Players)
        select full_name from playerId
        inner join GameBatterStats on GameBatterStats.batter_id =  playerId.player_id
        group by full_name
        order by sum(GameBatterStats.hits)/count(GameBatterStats.hits)
        limit 1;"""
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

# (best batter - home_runs:games ratio)
def best_batter_hrgratio(mycursor):
    sql = f"""with playerId as
        (select player_id, concat(first_name, ' ', last_name) as full_name from Players)
        select full_name from playerId
        inner join GameBatterStats on GameBatterStats.batter_id =  playerId.player_id
        group by full_name
        order by sum(GameBatterStats.home_runs)/count(GameBatterStats.home_runs) desc
        limit 1;"""
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

# (worst batter - home_runs:games ratio)
def worst_batter_hrgratio(mycursor):
    sql = f"""with playerId as
        (select player_id, concat(first_name, ' ', last_name) as full_name from Players)
        select full_name from playerId
        inner join GameBatterStats on GameBatterStats.batter_id =  playerId.player_id
        group by full_name
        order by sum(GameBatterStats.home_runs)/count(GameBatterStats.home_runs)
        limit 1;"""
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult