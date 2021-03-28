use MLB;
drop table if exists Players;
drop table if exists AtBat;

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
select 'Create AtBat' as '';

create table AtBat (ab_id decimal(10),
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

load data infile '/var/lib/mysql-files/MLB/atbats.csv' ignore into table AtBat
     fields terminated by ','
     lines terminated by '\n'
     ignore 1 lines;
