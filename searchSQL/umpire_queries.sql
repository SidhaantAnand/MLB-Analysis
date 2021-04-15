-- (num_games)
with umpireId as
(select umpire_id from Umpires where full_name = '{umpire_name}')
select count(*) as num_games from GameUmpireStats
inner join umpireId using (umpire_id);

-- (num_outs, num_challenges, num_correct_challenges)
with umpireId as
(select umpire_id from Umpires where full_name = '{umpire_name}')
select sum(ejections) as num_outs, sum(bs) as num_challenges, sum(bs_correct) as num_correct_challenges from GameUmpireStats
inner join umpireId using (umpire_id);

-- (usual position)
with umpireId as
(select umpire_id from Umpires where full_name = '{umpire_name}')
select position from GameUmpireStats
inner join umpireId using (umpire_id)
group by position
order by count(position) desc limit 1;

-- (usual venue)
with umpireId as
(select umpire_id from Umpires where full_name = '{umpire_name}')
select venue_name from Games
inner join GameUmpireStats using (g_id)
inner join umpireId using (umpire_id)
group by venue_name
order by count(venue_name) desc limit 1;

-- (best umpire)
with umpireId as
(select umpire_id, full_name from Umpires)
select full_name, sum(ejections)/sum(bs) as ratio from GameUmpireStats
inner join umpireId using (umpire_id)
group by full_name
order by ratio desc limit 1;

-- (worst umpire)
with umpireId as (select umpire_id, full_name from Umpires),
umpire_ejections as
    (select full_name, sum(ejections)/sum(bs) as ratio from GameUmpireStats inner join umpireId using (umpire_id) group by full_name)
select * from umpire_ejections
where ratio is not null
order by ratio limit 1;