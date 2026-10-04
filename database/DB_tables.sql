CREATE DATABASE IF NOT EXISTS MyMapleDrop;
USE MyMapleDrop;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS users, avators, items, bosses, drops, drop_participants;
SET FOREIGN_KEY_CHECKS = 1;


CREATE TABLE IF NOT EXISTS users (
	id INT PRIMARY KEY AUTO_INCREMENT,
    dc_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS avators (
	id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT, 
    avator VARCHAR(50) UNIQUE NOT NULL,
    cur_channel VARCHAR(50),
    job VARCHAR(50) NOT NULL,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS items (
	id INT PRIMARY KEY AUTO_INCREMENT,
    item VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS bosses (
	id INT PRIMARY KEY AUTO_INCREMENT,
    boss VARCHAR(50) UNIQUE NOT NULL,
    difficulty ENUM ('easy', 'normal', 'hard', 'extreme') Not Null,
    
    UNIQUE (boss, difficulty)
);

CREATE TABLE IF NOT EXISTS drops (
	id INT PRIMARY KEY AUTO_INCREMENT,
    created_at DATE,
    boss_id INT NOT NULL,
    item_id INT NOT NULL,
    is_container BOOLEAN NOT NULL,
    open_item_id INT,
    quantity INT DEFAULT 1,
    
    FOREIGN KEY (item_id)		REFERENCES items(id) 	ON DELETE CASCADE,
    FOREIGN KEY (boss_id) 		REFERENCES bosses(id) 	ON DELETE CASCADE,
    FOREIGN KEY (open_item_id) 	REFERENCES items(id) 	ON DELETE CASCADE
);

 CREATE TABLE IF NOT EXISTS drop_participants (
	id INT PRIMARY KEY AUTO_INCREMENT,
    avator_id INT,
    drop_id INT,
    
    FOREIGN KEY (avator_id)	REFERENCES avators(id) 	ON DELETE CASCADE,
    FOREIGN KEY (drop_id) REFERENCES drops(id) 	ON DELETE CASCADE
);