warnings;
drop table if exists Players;
drop table if exists AtBats;
drop table if exists Pitches;
drop table if exists Ejections;
drop table if exists Games;
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
			primary key (ab_id)
		);

load data infile '/var/lib/mysql-files/MLB/atbats.csv' ignore into table AtBats
     fields terminated by ','
     lines terminated by '\n'
     ignore 1 lines;


-- At Bat -------------------------------------------------------------------
select '----------------------------------------------------------------' as '';
select 'Create Pitches' as '';

create table Pitches (
	ab_id decimal(10),
	pitch_num decimal(3),
	px decimal(24, 22),
	pz decimal(22, 20),
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
	pfx_x decimal(23, 21),
	pfx_z decimal(23, 21),
	zone decimal(2),
	-- Constraints	    
	primary key (ab_id, pitch_num)
);

load data infile '/var/lib/mysql-files/MLB/pitches.csv' ignore into table Pitches
	fields terminated by ','
	lines terminated by '\n'
	ignore 1 lines
	(
		@px,
		@pz,
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
		@pfx_x,
		@pfx_z,
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
		px = if (@px like '', NULL, @px),
		pz = if (@pz like '', NULL, @pz),
		start_speed = if (@start_speed like '', NULL, @start_speed),
		end_speed = if (@end_speed like '', NULL, @end_speed),
		spin_rate = if (@spin_rate like '', NULL, @spin_rate),
		spin_dir = if (@spin_dir like '', NULL, @spin_dir),
		pfx_x = if (@pfx_x like '', NULL, @pfx_x),
		pfx_z = if (@pfx_z like '', NULL, @pfx_z),
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

-- Umpires -------------------------------------------------------------------
select '----------------------------------------------------------------' as '';
select 'Create Umpires' as '';

-- Umpire Stats-------------------------------------------------------------------
select '----------------------------------------------------------------' as '';
select 'Create UmpireStats' as '';

-- Game Batter Stats-------------------------------------------------------------------
select '----------------------------------------------------------------' as '';
select 'Create GameBatterStats' as '';



select 'Create Games' as '';
drop table Games;
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
			delay varchar(300),

			primary key (g_id)
		);


load data infile '/var/lib/mysql-files/MLB/games.csv' ignore into table Games
     fields terminated by ','
     OPTIONALLY ENCLOSED BY '"'
     lines terminated by '\n'
     ignore 1 lines
	(attendance,away_final_score,away_team,date,elapsed_time,g_id,home_final_score,home_team,start_time,umpire_1B,umpire_2B,umpire_3B,umpire_HP,venue_name,weather,wind,delay);
