# (num_ejections)
def player_ejections(mycursor, player_id):
    sql = '''select count(*) as num_ejections from Ejections
        inner join AtBats using (ab_id)
        where AtBats.batter_id =  \'{player_id}\';'''
    sql = sql.format(player_id=player_id)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult


# (num_times_out, num_hits, num_home_runs)
def player_hits_outs(mycursor, player_id):
    sql = '''select sum(outs) as num_outs, sum(hits) as num_hits, sum(home_runs) as num_home_runs from GameBatterStats
        where batter_id = \'{player_id}\';'''
    sql = sql.format(player_id=player_id)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult


# (most_played_inning, num_times_played_inning)
def player_inning(mycursor, player_id):
    sql = '''select inning, count(inning) from AtBats
        where batter_id = \'{player_id}\'
        group by inning
        order by count(inning) desc
        limit 1;'''
    sql = sql.format(player_id=player_id)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult


# (prefered_side - L or R)
def player_stand(mycursor, player_id):
    sql = '''select stand from AtBats
        where batter_id = \'{player_id}\'
        group by stand
        order by count(stand) desc
        limit 1;'''
    sql = sql.format(player_id=player_id)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult


# (best pitch type - w the least number of strikes)
def player_best_pitch_type(mycursor, player_id):
    sql = '''select pitch_type from Pitches
        inner join AtBats on AtBats.ab_id = Pitches.ab_id
        where batter_id = \'{player_id}\'
        and code = \'B\' or \'*B\'
        group by pitch_type
        order by count(pitch_type)/sum(b_count) desc
        limit 1;'''
    sql = sql.format(player_id=player_id)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult


# (worst pitch type - w the most number of strikes)
def player_worst_pitch_type(mycursor, player_id):
    sql = '''select pitch_type from Pitches
        inner join AtBats on AtBats.ab_id = Pitches.ab_id
        where batter_id = \'{player_id}\'
        and code != \'B\' and code != \'*B\'
        group by pitch_type
        order by count(pitch_type)/sum(b_count) desc
        limit 1;'''
    sql = sql.format(player_id=player_id)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult


# (best batter - balls:strikeout ratio)
def best_batter_bsratio(mycursor):
    sql = '''with playerId as
        (select player_id, concat(first_name, \' \', last_name) as full_name from Players)
        select full_name, sum(b_count)/sum(s_count) AS bsratio from playerId
        inner join AtBats on AtBats.batter_id =  playerId.player_id
        inner join Pitches on AtBats.ab_id = Pitches.ab_id
        group by full_name
        order by sum(b_count)/sum(s_count) desc
        limit 5;'''
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult


# (worst batter - balls:strikeout ratio)
def worst_batter_bsratio(mycursor):
    sql = '''with playerId as
        (select player_id, concat(first_name, \' \', last_name) as full_name from Players),
        bsRatioOrder AS ( 
        select full_name, sum(b_count)/sum(s_count) AS bsratio from playerId
        inner join AtBats on AtBats.batter_id =  playerId.player_id
        inner join Pitches on AtBats.ab_id = Pitches.ab_id
        group by full_name
        order by sum(b_count)/sum(s_count)
       )
        SELECT * FROM bsRatioOrder WHERE bsratio IS NOT NULL and bsratio != 0
        limit 5;'''
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult


# (best batter - hits:games ratio)
def best_batter_hgratio(mycursor):
    sql = '''with playerId as
        (select player_id, concat(first_name, \' \', last_name) as full_name from Players)
        select full_name, sum(GameBatterStats.hits)/count(GameBatterStats.hits) AS hgratio from playerId
        inner join GameBatterStats on GameBatterStats.batter_id =  playerId.player_id
        group by full_name
        order by sum(GameBatterStats.hits)/count(GameBatterStats.hits) desc
        limit 5;'''
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult


# (worst batter - hits:games ratio)
def worst_batter_hgratio(mycursor):
    sql = '''with playerId as
        (select player_id, concat(first_name, \' \', last_name) as full_name from Players),
        hgratioOrder AS (  
        select full_name, sum(GameBatterStats.hits)/count(GameBatterStats.hits) AS hgratio from playerId
        inner join GameBatterStats on GameBatterStats.batter_id =  playerId.player_id
        group by full_name
        order by sum(GameBatterStats.hits)/count(GameBatterStats.hits)
        )
        SELECT * FROM hgratioOrder WHERE hgratio != 0 AND hgratio IS NOT NULL
        limit 5;'''
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult


# (best batter - home_runs:games ratio)
def best_batter_hrgratio(mycursor):
    sql = '''with playerId as
        (select player_id, concat(first_name, \' \', last_name) as full_name from Players)
        select full_name, sum(GameBatterStats.home_runs)/count(GameBatterStats.home_runs) AS hrgratio from playerId
        inner join GameBatterStats on GameBatterStats.batter_id =  playerId.player_id
        group by full_name
        order by sum(GameBatterStats.home_runs)/count(GameBatterStats.home_runs) desc
        limit 5;'''
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult


# (worst batter - home_runs:games ratio)
def worst_batter_hrgratio(mycursor):
    sql = '''with playerId as
        (select player_id, concat(first_name, \' \', last_name) as full_name from Players),
        hrgratioOrder AS ( 
        select full_name, sum(GameBatterStats.home_runs)/count(GameBatterStats.home_runs) AS hrgratio from playerId
        inner join GameBatterStats on GameBatterStats.batter_id =  playerId.player_id
        group by full_name
        order by sum(GameBatterStats.home_runs)/count(GameBatterStats.home_runs)
        )
        SELECT * FROM hrgratioOrder WHERE hrgratio IS NOT NULL AND hrgratio != 0
        limit 5;'''
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult
