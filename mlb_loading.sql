drop table if exists Players;
drop table if exists AtBats;
drop table if exists Ejections;

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
			inning decimal(1),
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

-- Ejections -------------------------------------------------------------------
select '----------------------------------------------------------------' as '';
select 'Create Ejections' as '';

create table Ejections (ab_id decimal(10),
			g_id decimal(9) not null,
			event_num decimal(4),
			player_id decimal(6),
			bs char(1),
			correct char(1) not null,
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