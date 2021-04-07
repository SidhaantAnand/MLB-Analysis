# (num_games)
def umpire_games(mycursor, umpire_name):
  sql = f"""with umpireId as
    (select umpire_id from Umpires where full_name = '{umpire_name}')
    select count(*) as num_games from GameUmpireStats
    inner join umpireId using (umpire_id);"""
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  return myresult  

# (num_outs, num_challenges, num_correct_challenges)
def umpire_ejections(mycursor, umpire_name):
  sql = f"""with umpireId as
    (select umpire_id from Umpires where full_name = '{umpire_name}')
    select sum(ejections) as num_outs, sum(bs) as num_challenges, sum(bs_correct) as num_correct_challenges from GameUmpireStats
    inner join umpireId using (umpire_id);"""
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  return myresult  

# (usual position)
def umpire_position(mycursor, umpire_name):
  sql = f"""with umpireId as
    (select umpire_id from Umpires where full_name = '{umpire_name}')
    select position from GameUmpireStats
    inner join umpireId using (umpire_id)
    group by position
    order by count(position) desc limit 1;"""
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  return myresult

# (usual venue)
def umpire_venue(mycursor, umpire_name):
  sql = f"""with umpireId as
    (select umpire_id from Umpires where full_name = '{umpire_name}')
    select venue_name from Games
    inner join GameUmpireStats using (g_id)
    inner join umpireId using (umpire_id)
    group by venue_name
    order by count(venue_name) desc limit 1;"""
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  return myresult

# (best umpire)
def best_umpire(mycursor):
  sql = f"""with umpireId as
    (select umpire_id, full_name from Umpires)
    select full_name from GameUmpireStats
    inner join umpireId using (umpire_id)
    group by full_name
    order by sum(ejections)/sum(bs) desc limit 1;"""
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  return myresult

# (worst umpire)
def worst_umpire(mycursor):
  sql = f"""with umpireId as
    (select umpire_id, full_name from Umpires)
    select full_name from GameUmpireStats
    inner join umpireId using (umpire_id)
    group by full_name
    order by sum(ejections)/sum(bs) limit 1;"""
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  return myresult