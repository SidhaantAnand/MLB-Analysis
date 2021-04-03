-- 1. Game with highest home score
select g_id, home_final_score from Games where home_final_score = (select max(home_final_score) from Games);

-- 2. Game with highest away score
select g_id, away_final_score from Games where away_final_score = (select max(away_final_score) from Games);

-- 3. Game with highest combined score
select g_id, home_final_score, away_final_score from Games where
    (home_final_score + away_final_score = (select max(home_final_score + Games.away_final_score) from Games));

-- 4. Game with highest attendance
select g_id, attendance from Games where attendance = (select max(attendance) from Games);

-- 5. Game with lowest attendance
select g_id, attendance from Games where attendance = (select min(attendance) from Games);

-- 6. Games with higher than x home score (using 20 as placeholder)
select count(*) from Games where home_final_score > 20;

-- 7. Games with higher than x away score (using 20 as placeholder)
select count(*) from Games where away_final_score > 20;

-- 8. Longest game (elapsed time)
select g_id, elapsed_time from Games where elapsed_time = (select max(elapsed_time) from Games);

-- 9. Longest game (innings)
select distinct Games.g_id, inning from Games inner join AtBats on Games.g_id = AtBats.g_id where inning = (select max(inning) as highest_inning from AtBats);

-- 10. Shortest game (elapsed time)
select g_id, elapsed_time from Games where elapsed_time = (select min(elapsed_time) from Games);

-- 11. Longest winning streak
set @row_number:=0, @seq:=0;
with A as (select @row_num:=@row_num+1 as row_num, team_id, g_id, won from GameTeamStats order by team_id, g_id),
B as (select A1.team_id, @seq:=if(A1.won = 'W', @seq + 1, 0) as win_streak from A A1, A A2 where A1.row_num + 1 = A2.row_num and A1.team_id = A2.team_id)
select team_id, win_streak from B order by win_streak desc limit 1;

-- 12. Longest losing streak
set @row_number:=0, @seq:=0;
with A as (select @row_num:=@row_num+1 as row_num, team_id, g_id, won from GameTeamStats order by team_id, g_id),
B as (select A1.team_id, @seq:=if(A1.won = 'L', @seq + 1, 0) as lose_streak from A A1, A A2 where A1.row_num + 1 = A2.row_num and A1.team_id = A2.team_id)
select team_id, lose_streak from B order by lose_streak desc limit 1;



