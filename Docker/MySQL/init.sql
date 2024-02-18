DROP DATABASE chatapp;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE clubs(
    club_id serial PRIMARY KEY,
    club_name varchar(255) NOT NULL
);

CREATE TABLE users (
    uid varchar(255) PRIMARY KEY,
    user_name varchar(255) NOT NULL,
    email varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    club_id integer REFERENCES clubs(club_id)
);

CREATE TABLE channels (
    id serial PRIMARY KEY,
    uid integer REFERENCES users(uid),
    name varchar(255) UNIQUE NOT NULL,
    abstract varchar(255),
    club_id integer REFERENCES clubs(club_id)
    );

CREATE TABLE messages (
    id serial PRIMARY KEY,
    uid integer REFERENCES users(uid),
    cid integer REFERENCES channels(id) ON DELETE CASCADE,
    message text,
    created_at timestamp not null default current_timestamp
);

CREATE TABLE replies (
    id serial PRIMARY KEY,
    uid integer REFERENCES users(uid),
    message_id integer REFERENCES message(id) ON DELETE CASCADE,
    message text,
    created_at timestamp not null default current_timestamp
);

INSERT INTO users(uid,user_name,email,password,club_id)
VALUES('8defdaea-b411-43d3-8521-db7dc88e633b','na','ff@gmail.com','1234',1);

INSERT INTO clubs(club_id,club_name)
VALUES(1,'baseball team'),
      (2,'table tennis team'),
      (3,'judo team'),
      (4,'kendo team'),
      (5,'soccer team'),
      (6,'volleyball team'),
      (7,'basketball team'),
      (8,'calligraphy club'),
      (9,'photography club'),
      (10,'art club'),
      (11,'band club'),
      (12,'literature club');



