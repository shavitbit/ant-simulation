CREATE DATABASE IF NOT EXISTS ant_db;

USE ant_db;
CREATE TABLE IF NOT EXISTS ant_table (
    sim_name VARCHAR(50) PRIMARY KEY,
    run_count INT NOT NULL,
    total_food_collected INT NOT NULL
);
/*
sim name indicate the settings of the simulation
from those column i can get the avarage of each id

insert data:
 INSERT INTO ant_table (sim_name,run_count,total_food_collected)
 VALUES ('20.0-1.5-1.0-5.0',1,150)
 ;
*/