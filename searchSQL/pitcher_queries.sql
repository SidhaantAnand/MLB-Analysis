-- 1. Career stats for a pitcher (using placeholder player ID of 453265)

-- Number of strikes pitched
select sum(total_s_counts) from GamePitcherStats where pitcher_id = 453265;

-- Number of strikeouts
select count(*) from AtBats where pitcher_id = 453265 and event = 'Strikeout';

-- Number of balls pitched
select sum(total_b_counts) from GamePitcherStats where pitcher_id = 453265;

-- Number of home runs allowed
select count(*) from AtBats where pitcher_id = 453265 and event = 'Home Run';

-- Total pitches
select sum(num_pitches) from GamePitcherStats where pitcher_id = 453265;

-- Average spin rate and direction
select avg(avg_spin_rate), avg(avg_spin_dir) from GamePitcherStats where pitcher_id = 453265;

-- Average pitch speed
select avg(avg_start_speed) from GamePitcherStats where pitcher_id = 453265;

-- Most common zone pitched
with A as (select most_common_zone, count(*) as pitches_in_zone from GamePitcherStats where pitcher_id = 453265 group by most_common_zone)
select most_common_zone, pitches_in_zone from A where pitches_in_zone = (select max(pitches_in_zone) from A);

-- Preferred throwing side
with A as (select p_throws, count(*) as num_thrown_from_side from AtBats where pitcher_id = 453265 group by p_throws)
select p_throws, num_thrown_from_side from A where num_thrown_from_side = (select max(num_thrown_from_side) from A);

-- Most common pitch type
with A as (select pitch_type, count(*) as times_thrown from AtBats inner join Pitches on AtBats.ab_id = Pitches.ab_id where pitcher_id = 453265 group by pitch_type)
select pitch_type, times_thrown from A where times_thrown = (select max(times_thrown) from A);

-- Number of strikes and balls pitched, number of pitches, average spin rate, direction and throw speed can be consolidated into one query
select sum(total_s_counts), sum(total_b_counts), sum(num_pitches), avg(avg_spin_rate), avg(avg_spin_dir), avg(avg_start_speed)
    from GamePitcherStats where pitcher_id = 453265;


-- 2. Best/Worst pitcher

-- Best pitcher (strikeouts:pitches ratio)
with A as (select pitcher_id, sum(num_pitches) as num_pitches from GamePitcherStats group by pitcher_id),
B as (select pitcher_id, count(*) as num_strikeouts from AtBats where event = 'Strikeout' group by pitcher_id),
C as (select A.pitcher_id, B.num_strikeouts/A.num_pitches as ratio from A inner join B on A.pitcher_id = B.pitcher_id)
select pitcher_id, ratio from C where ratio = (select max(ratio) from C);

-- Worst pitcher (strikeouts:pitches ratio)
with A as (select pitcher_id, sum(num_pitches) as num_pitches from GamePitcherStats group by pitcher_id),
B as (select pitcher_id, count(*) as num_strikeouts from AtBats where event = 'Strikeout' group by pitcher_id),
C as (select A.pitcher_id, coalesce(B.num_strikeouts, 0)/A.num_pitches as ratio from A left join B on A.pitcher_id = B.pitcher_id)
select pitcher_id, ratio from C where ratio = (select min(ratio) from C);

-- potentially add a home-runs-allowed:at_bats ratio


