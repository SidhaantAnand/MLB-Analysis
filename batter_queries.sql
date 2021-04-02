-- (num_ejections)
with playerId as
(select player_id from Players where 
first_name = '{player_name_split[0]}' and last_name = '{player_name_split[1]}')
select count(*) as num_ejections from Ejections
inner join AtBats using (ab_id)
inner join playerId on AtBats.batter_id =  playerId.player_id;

-- (num_times_out)
with playerId as
(select player_id from Players where 
first_name = '{player_name_split[0]}' and last_name = '{player_name_split[1]}')
select sum(outs) as num_outs from GameBatterStats
inner join playerId on playerId.player_id = GameBatterStats.batter_id
where batter_id = playerId.player_id;

-- (most_played_inning, num_times_played_inning)
with playerId as
(select player_id from Players where 
first_name = '{player_name_split[0]}' and last_name = '{player_name_split[1]}')
select inning, count(inning) from AtBats
inner join playerId on AtBats.batter_id =  playerId.player_id
group by inning
order by count(inning) desc
limit 1;

-- (prefered_side - L or R)
with playerId as
(select player_id from Players where 
first_name = '{player_name_split[0]}' and last_name = '{player_name_split[1]}')
select stand from AtBats
inner join playerId on AtBats.batter_id =  playerId.player_id
group by stand
order by count(stand) desc
limit 1;

-- (best pitch type - w the least number of strikes)
with playerId as
(select player_id from Players where 
first_name = '{player_name_split[0]}' and last_name = '{player_name_split[1]}')
select pitch_type from Pitches
inner join AtBats on AtBats.ab_id = Pitches.ab_id
inner join playerId on AtBats.batter_id =  playerId.player_id
where code = 'B' or '*B'
group by pitch_type
order by count(pitch_type)/sum(b_count) desc
limit 1;

-- (worst pitch type - w the most number of strikes)
with playerId as
(select player_id from Players where 
first_name = '{player_name_split[0]}' and last_name = '{player_name_split[1]}')
select pitch_type from Pitches
inner join AtBats on AtBats.ab_id = Pitches.ab_id
inner join playerId on AtBats.batter_id =  playerId.player_id
where code != 'B' and code != '*B'
group by pitch_type
order by count(pitch_type)/sum(b_count) desc
limit 1;