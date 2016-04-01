CREATE DATABASE IF NOT EXISTS  test1_database;
USE test1_database;

CREATE USER 'test1_jack'@'localhost' IDENTIFIED BY '123';
GRANT ALL ON test1_database.* TO 'test1_jack'@'localhost';

CREATE TABLE IF NOT EXISTS  test1_user_table 
	(
		user_id TINYINT ,
		desc_info VARCHAR(200),
		dev_table_name VARCHAR(30),
		create_use_date DATETIME
	);
CREATE TABLE IF NOT EXISTS test1_dev_table
	(
		dev_id int,
		desc_info varchar(200),
		sensor_table_name varchar(30),
		create_dev_date datetime,
		parent_id tinyint
	);
CREATE TABLE IF NOT EXISTS sensor_table_name
	(
		sensor_id int,
		desc_info varchar(200),
		data_table_name varchar(30),
		create_sensor_date datetime,
		parent_id int,
		sensor_type char(4)
	);
CREATE TABLE IF NOT EXISTS data_table_name
	(
		data_time datetime,
		data float(24)
	);
