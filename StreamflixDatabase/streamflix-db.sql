/*******************************************************************************
   Streamflix Database
   Script: streamflix-db.sql
   Description: Creates the Streamflix database.
   DB Server: MySql
   Authors: Ashley Davis, Nicole Contreras, Khanh Nguyen, and Sai Kumar Reddy
********************************************************************************/


/*******************************************************************************
   Drop database if it exists
********************************************************************************/
DROP DATABASE IF EXISTS `Streamflix`;

/*******************************************************************************
   Create database
********************************************************************************/
CREATE DATABASE `Streamflix`;


USE `Streamflix`;


/*******************************************************************************
   Create Tables
********************************************************************************/
CREATE TABLE `User`
(
    user_id INT,
    username VARCHAR(30) NOT NULL,
    password VARCHAR(36) DEFAULT (UUID()),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(250) NOT NULL,
    phone VARCHAR(15),
    date_of_birth DATE NOT NULL,
    date_joined DATETIME DEFAULT CURRENT_TIMESTAMP,
    subscription_plan ENUM('Family', 'Student', 'Regular'),
    PRIMARY KEY (user_id)
);

CREATE TABLE `Genre`
(
    genre_id INT AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL,
    PRIMARY KEY (genre_id)
);

CREATE TABLE `Profile`
(
    profile_id INT AUTO_INCREMENT,
    name VARCHAR(100),
    user_id INT NOT NULL,
    PRIMARY KEY (profile_id),
    FOREIGN KEY (user_id) REFERENCES `User`(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE `Device`
(
    device_id INT AUTO_INCREMENT,
    ip_address VARCHAR(18),
    user_id INT NOT NULL,
    PRIMARY KEY (device_id),
    FOREIGN KEY (user_id) REFERENCES `User`(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE `Video_Content`
(
    content_id INT AUTO_INCREMENT,
    title VARCHAR(300) NOT NULL,
    thumbnail VARCHAR(10),
    country varchar(100),
    description LONGTEXT,
    release_year varchar(4),
    language VARCHAR(100),
    PRIMARY KEY (content_id),
    INDEX(title)
);

CREATE TABLE `Movie`
(
    movie_id INT AUTO_INCREMENT,
    duration INT,
    content_id INT,
    PRIMARY KEY (movie_id),
    FOREIGN KEY (content_id) REFERENCES `Video_Content` (content_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE `Series`
(
    series_id INT AUTO_INCREMENT,
    content_id INT,
    PRIMARY KEY (series_id),
    FOREIGN KEY (content_id) REFERENCES `Video_Content` (content_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE `Season`
(
    season_id INT AUTO_INCREMENT,
    series_id INT,
    PRIMARY KEY (season_id),
    FOREIGN KEY (series_id) REFERENCES `Series`(series_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE `Episode`
(
    episode_id INT AUTO_INCREMENT,
    title VARCHAR(150) NOT NULL,
    duration INT,
    season_id INT,
    PRIMARY KEY (episode_id),
    FOREIGN KEY (season_id) REFERENCES `Season`(season_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE `Actor`
(
    actor_id INT AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10),
    biography LONGTEXT,
    content_id INT,
    PRIMARY KEY (actor_id)
);

CREATE TABLE `Director`
(
    director_id INT AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    date_of_birth DATE NOT NULL,
    biography LONGTEXT NOT NULL,
    content_id INT,
    PRIMARY KEY (director_id)
);

CREATE TABLE `Review`
(
    review_id INT AUTO_INCREMENT,
    date_posted DATETIME DEFAULT CURRENT_TIMESTAMP,
    review_content LONGTEXT NOT NULL,
    stars INT NOT NULL CHECK (stars BETWEEN 1 AND 5),
    user_id INT,
    PRIMARY KEY (review_id),
    FOREIGN KEY (user_id) REFERENCES `User`(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE `Content_Review`
(
    content_id INT,
    review_id INT,
    PRIMARY KEY (content_id, review_id),
    FOREIGN KEY (content_id) REFERENCES `Video_Content`(content_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE ,
    FOREIGN KEY (review_id) REFERENCES `Review`(review_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE `Content_Genre`
(
    content_id INT,
    genre_id INT,
    PRIMARY KEY (content_id, genre_id),
    FOREIGN KEY (content_id) REFERENCES `Video_Content`(content_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES `Genre`(genre_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE `Content_Actor`
(
    content_id INT,
    actor_id INT,
    PRIMARY KEY (content_id, actor_id),
    FOREIGN KEY (content_id) REFERENCES `Video_Content`(content_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (actor_id) REFERENCES `Actor`(actor_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE `Content_Director`
(
    content_id INT,
    director_id INT,
    PRIMARY KEY (content_id, director_id),
     FOREIGN KEY (content_id) REFERENCES `Video_Content`(content_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (director_id) REFERENCES `Director`(director_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE `User_Metrics` (
    metric_id INT AUTO_INCREMENT,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    duration INT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    content_id INT,
    user_id INT,
    PRIMARY KEY (metric_id),
    FOREIGN KEY (content_id) REFERENCES `Video_Content` (content_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES `User` (user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE `My_List` (
    mylist_id INT AUTO_INCREMENT,
    name VARCHAR(30),
    user_id INT,
    PRIMARY KEY (mylist_id),
    FOREIGN KEY (user_id) REFERENCES `User`(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE `Listed_Content`
(
    content_id INT,
    mylist_id INT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (mylist_id, content_id),
    FOREIGN KEY (mylist_id) REFERENCES `My_List`(mylist_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (content_id) REFERENCES `Video_Content`(content_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);