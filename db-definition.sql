CREATE DATABASE IF NOT EXISTS sistema;
USE sistema;
DROP TABLE IF EXISTS rankingteams;

CREATE TABLE IF NOT EXISTS rankingteams (
    id int not null auto_increment,
    teamname varchar(100),
    country varchar(100),
    manager varchar(100),
    logo varchar(5000),
    primary key (id)
);

-- insert into rankingteams (name, country, manager, logo) values ('Test', 'testcountry', 'testmanager', 'testlogo.jpg');

-- select * from empleados;