import mysql.connector

mydb = mysql.connector.connect(
  host="99.250.146.93",
  user="root",
  password="MLB_Gang",
  database="MLB"
)

mycursor = mydb.cursor()

# place holder values - should be set by the client application
umpire_name = "Mike Everitt"

# sql queries
# (num_games)
umpire_games_sql = f"""with umpireId as
(select umpire_id from Umpires where full_name = '{umpire_name}')
select count(*) as num_games from GameUmpireStats
inner join umpireId using (umpire_id);"""

# (num_outs, num_challenges, num_correct_challenges)
umpire_ejections_sql = f"""with umpireId as
(select umpire_id from Umpires where full_name = '{umpire_name}')
select sum(ejections) as num_outs, sum(bs) as num_challenges, sum(bs_correct) as num_correct_challenges from GameUmpireStats
inner join umpireId using (umpire_id);"""

# (usual position)
umpire_position_sql = f"""with umpireId as
(select umpire_id from Umpires where full_name = '{umpire_name}')
select position from GameUmpireStats
inner join umpireId using (umpire_id)
group by position
order by count(position) desc limit 1;"""

# (usual venue)
umpire_venue_sql = f"""with umpireId as
(select umpire_id from Umpires where full_name = '{umpire_name}')
select venue_name from Games
inner join GameUmpireStats using (g_id)
inner join umpireId using (umpire_id)
group by venue_name
order by count(venue_name) desc limit 1;"""

# (best umpire)
best_umpire_sql = f"""with umpireId as
(select umpire_id, full_name from Umpires)
select full_name from GameUmpireStats
inner join umpireId using (umpire_id)
group by full_name
order by sum(ejections)/sum(bs) desc limit 1;"""

# (worst umpire)
worst_umpire_sql = f"""with umpireId as
(select umpire_id, full_name from Umpires)
select full_name from GameUmpireStats
inner join umpireId using (umpire_id)
group by full_name
order by sum(ejections)/sum(bs) limit 1;"""

# printing results - can print whatever query, more for the client side to handle
mycursor.execute(worst_umpire_sql)
myresult = mycursor.fetchall()
for x in myresult:
    print(x)