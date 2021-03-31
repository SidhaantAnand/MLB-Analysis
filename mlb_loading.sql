warnings;
drop table if exists Players;
drop table if exists AtBats;
drop table if exists Pitches;
drop table if exists Ejections;
drop table if exists Games;
drop table if exists Umpires;
drop table if exists GameUmpireStats;
drop table if exists GameBatterStats;
-- Players -------------------------------------------------------------------
select '----------------------------------------------------------------' as '';
select 'Create Players' as '';

create table Players (player_id decimal(6),
			first_name char(20) not null,
			last_name char(20) not null,
-- Constraints	    
		    primary key (player_id)
		);

load data infile '/var/lib/mysql-files/MLB/player_names.csv' ignore into table Players
     fields terminated by ','
     lines terminated by '\n'
     ignore 1 lines
     (player_id, first_name, last_name);

-- At Bat -------------------------------------------------------------------
select '----------------------------------------------------------------' as '';
select 'Create AtBats' as '';

create table AtBats (ab_id decimal(10),
			batter_id decimal(6),
			event char(20),
			g_id decimal(9) not null,
			inning decimal(2),
			o decimal(1),
			p_score decimal(2),
			p_throws char(1),
			pitcher_id decimal(6),
			stand char(1),
			top char(5),
		-- Constraints	    
			primary key (ab_id),
			check (p_throws = 'L' or p_throws = 'R'),
			check (stand = 'L' or stand = 'R'),
			check (top = 'True' or top = 'False')
		);

load data infile '/var/lib/mysql-files/MLB/atbats.csv' ignore into table AtBats
     fields terminated by ','
     lines terminated by '\n'
     ignore 1 lines;


-- Pitches -------------------------------------------------------------------
select '----------------------------------------------------------------' as '';
select 'Create Pitches' as '';

create table Pitches (
	ab_id decimal(10),
	pitch_num decimal(3),
	start_speed decimal(4, 1),
	end_speed decimal(4, 1),
	spin_rate decimal(7, 3),
	spin_dir decimal(6, 3),
	code char(2),
	type char(1),
	pitch_type char(2),
	event_num decimal(4),
	b_score decimal(2),
	b_count decimal(1),
	s_count decimal(1),
	outs decimal(1),
	on_1b boolean,
	on_2b boolean,
	on_3b boolean,
	zone decimal(2),
	-- Constraints	    
	primary key (ab_id, pitch_num)
);

load data infile '/var/lib/mysql-files/MLB/pitches.csv' ignore into table Pitches
	fields terminated by ','
	lines terminated by '\n'
	ignore 1 lines
	(
		@ignore,
		@ignore,
		@start_speed,
		@end_speed,
		@spin_rate,
		@spin_dir,
		@ignore,
		@ignore,
		@ignore,
		@ignore,
		@ignore,
		@ignore,
		@ignore,
		@ignore,
		@ignore,
		@ignore,
		@ignore,
		@ignore,
		@ignore,
		@ignore,
		@ignore,
		@ignore,
		@ignore,
		@ignore,
		@ignore,
		@ignore,
		@zone,
		code,
		type,
		pitch_type,
		event_num,
		b_score,
		ab_id,
		b_count,
		s_count,
		outs,
		pitch_num,
		on_1b,
		on_2b,
		on_3b
	)
	set
		start_speed = if (@start_speed like '', NULL, @start_speed),
		end_speed = if (@end_speed like '', NULL, @end_speed),
		spin_rate = if (@spin_rate like '', NULL, @spin_rate),
		spin_dir = if (@spin_dir like '', NULL, @spin_dir),
		zone = if (@zone like '', NULL, @zone);


-- Ejections -------------------------------------------------------------------
select '----------------------------------------------------------------' as '';
select 'Create Ejections' as '';

create table Ejections (ab_id decimal(10),
			g_id decimal(9) not null,
			event_num decimal(4),
			player_id decimal(6),
			bs char(1),
			correct char(2) not null,
			team char(3),
			is_home_team char(5),
			des varchar(255),
		-- Constraints	    
			primary key (ab_id, g_id, player_id)
		);

load data infile '/var/lib/mysql-files/MLB/ejections.csv' ignore into table Ejections
     fields terminated by ','
     lines terminated by '\n'
     ignore 1 lines
	(ab_id, des, event_num, g_id, player_id, @throwaway, bs, correct, team, is_home_team);

select 'Create Games' as '';
create table Games (attendance decimal(5) check (attendance >= 0),
			away_final_score decimal(2) not null check (away_final_score >= 0),
			away_team char(3) not null,
			date datetime,
			elapsed_time decimal(3),
			g_id decimal(9) not null,
			home_final_score decimal(2) not null check (home_final_score >= 0),
			home_team char(3) not null,
			start_time varchar(10) not null check (start_time REGEXP '[0-9]:[0-9][0-9] [A|P][M]'),
			umpire_1B varchar(300),
			umpire_2B varchar(300),
			umpire_3B varchar(300),
			umpire_HP varchar(300),
			venue_name varchar(300),
			weather varchar(300) not null check (weather REGEXP '[0-9]+ degrees, (clear|sunny|overcast|cloudy|partly cloudy|snow|drizzle|dome|roof closed|rain)'),
			wind varchar(300) not null check (wind REGEXP '[0-9]+ mph,.*') ,
			delay decimal(5),

			primary key (g_id)
		);


load data infile '/var/lib/mysql-files/MLB/games.csv' ignore into table Games
     fields terminated by ','
     OPTIONALLY ENCLOSED BY '"'
     lines terminated by '\n'
     ignore 1 lines
	(attendance,away_final_score,away_team,date,elapsed_time,g_id,home_final_score,home_team,start_time,umpire_1B,umpire_2B,umpire_3B,umpire_HP,venue_name,weather,wind,delay);

-- Umpires -------------------------------------------------------------------
select '----------------------------------------------------------------' as '';
select 'Create Umpires' as '';
create table Umpires (umpire_id int not null auto_increment,
			first_name char(20) not null,
			last_name char(20) not null,
-- Constraints	    
		    primary key (umpire_id)
		);
insert into Umpires (first_name, last_name)
	(select substring(umpire_1B, 1, locate(' ', umpire_1B)), substring(umpire_1B, locate(' ', umpire_1B) + 1) from Games group by umpire_1B);

insert into Umpires (first_name, last_name)
	(select substring(umpire_2B, 1, locate(' ', umpire_2B)), substring(umpire_2B, locate(' ', umpire_2B) + 1) from Games 
	where not exists (select first_name, last_name from Umpires) group by umpire_2B);

insert into Umpires (first_name, last_name)
	(select substring(umpire_3B, 1, locate(' ', umpire_3B)), substring(umpire_3B, locate(' ', umpire_3B) + 1) from Games 
	where not exists (select first_name, last_name from Umpires) group by umpire_3B);

insert into Umpires (first_name, last_name)
	(select substring(umpire_HP, 1, locate(' ', umpire_HP)), substring(umpire_HP, locate(' ', umpire_HP) + 1) from Games 
	where not exists (select first_name, last_name from Umpires) group by umpire_HP);

-- Umpire Stats-------------------------------------------------------------------
select '----------------------------------------------------------------' as '';
select 'Create GameUmpireStats' as '';

create table GameUmpireStats (umpire_id int,
			g_id decimal(9),
			position char(2),
			ejections decimal(2),
			bs decimal(2),
			bs_correct decimal(2),
            primary key(g_id, umpire_id)
		-- Constraints	    
		);

insert into GameUmpireStats (umpire_id, g_id, position, ejections, bs, bs_correct)
    (select distinct Umpires.umpire_id, Games.g_id, '1B', 0, 0, 0 from Umpires 
    inner join Games on Games.umpire_1B = concat(Umpires.first_name, ' ', Umpires.last_name));

insert into GameUmpireStats (umpire_id, g_id, position, ejections, bs, bs_correct)
    (select distinct Umpires.umpire_id, Games.g_id, '2B', 0, 0, 0 from Umpires 
    inner join Games on Games.umpire_2B = concat(Umpires.first_name, ' ', Umpires.last_name));

insert into GameUmpireStats (umpire_id, g_id, position, ejections, bs, bs_correct)
    (select distinct Umpires.umpire_id, Games.g_id, '3B', 0, 0, 0 from Umpires 
    inner join Games on Games.umpire_3B = concat(Umpires.first_name, ' ', Umpires.last_name));

insert into GameUmpireStats (umpire_id, g_id, position, ejections, bs, bs_correct)
    (select distinct Umpires.umpire_id, Games.g_id, 'HP', 0, 0, 0 from Umpires 
    inner join Games on Games.umpire_HP = concat(Umpires.first_name, ' ', Umpires.last_name));

with num_ejections as
(select g_id, substring(Ejections.des, locate('by ', Ejections.des) + 3, 2) as position, count(*) as count from Ejections group by g_id, substring(Ejections.des, locate('by ', Ejections.des) + 3, 2))
update GameUmpireStats
    inner join num_ejections on GameUmpireStats.g_id = num_ejections.g_id 
    and GameUmpireStats.position = num_ejections.position
    set GameUmpireStats.ejections = num_ejections.count;

with num_bs as
(select g_id, substring(Ejections.des, locate('by ', Ejections.des) + 3, 2) as position, count(*) as count from Ejections where Ejections.bs = 'Y' group by g_id, substring(Ejections.des, locate('by ', Ejections.des) + 3, 2))
update GameUmpireStats
    inner join num_bs on GameUmpireStats.g_id = num_bs.g_id 
    and GameUmpireStats.position = num_bs.position
    set GameUmpireStats.bs = num_bs.count;

with num_correct as
(select g_id, substring(Ejections.des, locate('by ', Ejections.des) + 3, 2) as position, count(*) as count from Ejections where Ejections.bs = 'Y' and Ejections.correct = 'C' group by g_id, substring(Ejections.des, locate('by ', Ejections.des) + 3, 2))
update GameUmpireStats
    inner join num_correct on GameUmpireStats.g_id = num_correct.g_id 
    and GameUmpireStats.position = num_correct.position
    set GameUmpireStats.bs_correct = num_correct.count;

-- Game Batter Stats-------------------------------------------------------------------
select '----------------------------------------------------------------' as '';
select 'Create GameBatterStats' as '';

create table GameBatterStats (batter_id decimal(6),
			g_id decimal(9),
			team_id char(3),
			outs decimal(2),
			stand char(1),
            primary key(g_id, batter_id)
		-- Constraints	    
		);

insert into GameBatterStats(batter_id, g_id, outs, stand)
	(select batter_id, g_id, sum(o) from AtBats group by batter_id, g_id);

update GameBatterStats
	inner join AtBats on AtBats.g_id = GameBatterStats.g_id and AtBats.batter_id = GameBatterStats.batter_id
	set GameBatterStats.stand = AtBats.stand;

update GameBatterStats
	inner join AtBats on AtBats.g_id = GameBatterStats.g_id and AtBats.batter_id = GameBatterStats.batter_id
	inner join Games on Games.g_id = AtBats.g_id
	set GameBatterStats.team_id = Games.away_team where AtBats.top = 'True';

update GameBatterStats
	inner join AtBats on AtBats.g_id = GameBatterStats.g_id and AtBats.batter_id = GameBatterStats.batter_id
	inner join Games on Games.g_id = AtBats.g_id
	set GameBatterStats.team_id = Games.home_team where AtBats.top = 'False';


-- Venue -------------------------------------------------------------------
select '----------------------------------------------------------------' as '';
select 'Create Venue' as '';
create table Venue(
	venue_id int  NOT NULL AUTO_INCREMENT,
	venue_name varchar(300),
	primary key(venue_id)
);
insert into Venue (venue_name) ( SELECT distinct venue_name FROM Games);


-- Teams -------------------------------------------------------------------
select '----------------------------------------------------------------' as '';
select 'Create Teams' as '';
create table Teams(
	team_id char(3) not null,
	team_name varchar(300),
	primary key(team_id)
);
insert into Teams (team_id) ( SELECT distinct home_team AS team_id FROM Games);

update Teams set team_name = 'Los Angeles Angles' WHERE team_id = 'ana';
update Teams set team_name = 'Arizona Diamondbacks' WHERE team_id = 'ari';
update Teams set team_name = 'Atlanta Braves' WHERE team_id = 'atl';
update Teams set team_name = 'Baltimore Orioles' WHERE team_id = 'bal';
update Teams set team_name = 'Boston Red Sox' WHERE team_id = 'bos';
update Teams set team_name = 'Chicago White Sox' WHERE team_id = 'cha';
update Teams set team_name = 'Chicago Cubs' WHERE team_id = 'chn';
update Teams set team_name = 'Cincinnati Reds' WHERE team_id = 'cin';
update Teams set team_name = 'Cleveland Indians' WHERE team_id = 'cle';
update Teams set team_name = 'Colorado Rockies' WHERE team_id = 'col';
update Teams set team_name = 'Detroit Tigers' WHERE team_id = 'det';
update Teams set team_name = 'Houston Astros' WHERE team_id = 'hou';
update Teams set team_name = 'Kansas City Royals' WHERE team_id = 'kca';
update Teams set team_name = 'Los Angeles Dodgers' WHERE team_id = 'lan';
update Teams set team_name = 'Miami Marlins' WHERE team_id = 'mia';
update Teams set team_name = 'Milwaukee Brewers' WHERE team_id = 'mil';
update Teams set team_name = 'Minnesota Twins' WHERE team_id = 'min';
update Teams set team_name = 'New York Yankees' WHERE team_id = 'nya';
update Teams set team_name = 'New York Mets' WHERE team_id = 'nyn';
update Teams set team_name = 'Oakland Athletics' WHERE team_id = 'oak';
update Teams set team_name = 'Philadelphia Phillies' WHERE team_id = 'phi';
update Teams set team_name = 'Pittsburgh Pirates' WHERE team_id = 'pit';
update Teams set team_name = 'San Diego Padres' WHERE team_id = 'sdn';
update Teams set team_name = 'Seattle Mariners' WHERE team_id = 'sea';
update Teams set team_name = 'San Francisco Giants' WHERE team_id = 'sfn';
update Teams set team_name = 'St. Louis Cardinals' WHERE team_id = 'sln';
update Teams set team_name = 'Tampa Bay Rays' WHERE team_id = 'tba';
update Teams set team_name = 'Texas Rangers' WHERE team_id = 'tex';
update Teams set team_name = 'Toronto Blue Jays' WHERE team_id = 'tor';
update Teams set team_name = 'Washington Nationals' WHERE team_id = 'was';




-- Venue -------------------------------------------------------------------
select '----------------------------------------------------------------' as '';
select 'Create GameTeamStats' as '';
create table GameTeamStats(
	g_id decimal(9) not null,
	team_id char(3) not null,
	venue_id int,
	is_home_team decimal(1),
	won decimal(1),
	final_score decimal(2),
	ejections decimal(2),
	outs decimal(2),
	delay decimal(5),
	primary key(g_id,team_id)
);


insert into GameTeamStats(g_id,team_id,final_score,delay,is_home_team)
( SELECT g_id,home_team AS team_id,home_final_score AS final_score,delay,1 FROM Games);

insert into GameTeamStats(g_id,team_id,final_score,delay,is_home_team)
( SELECT g_id,away_team AS team_id,away_final_score AS final_score,delay,0 FROM Games);

WITH venueGameJoin AS (SELECT Venue.venue_id,Venue.venue_name,Games.g_id AS g_id FROM Venue INNER JOIN Games USING(venue_name))
update GameTeamStats set venue_id = (SELECT venue_id WHERE GameTeamStats.g_id = venueGameJoin.g_id );