DROP DATABASE chatapp;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE clubs(
    club_id INT PRIMARY KEY,
    club_name varchar(255) UNIQUE NOT NULL
);

CREATE TABLE users (
    uid INT PRIMARY KEY,
    user_name varchar(255) UNIQUE NOT NULL,
    email varchar(255) UNIQUE NOT NULL,
    password varchar(255) NOT NULL,
    club_id INT NOT NULL  REFERENCES clubs(club_id)
);

CREATE TABLE channels (
    id serial PRIMARY KEY,
    uid varchar(255)  REFERENCES users(uid),
    name varchar(255) UNIQUE NOT NULL,
    abstract varchar(255),
    club_channels int NOT NULL  REFERENCES users(club_id)
    );

CREATE TABLE messages (
    id serial PRIMARY KEY,
    uid varchar(255)  REFERENCES users(uid),
    cid integer REFERENCES channels(id) ON DELETE CASCADE,
    message text,
    created_at timestamp not null default current_timestamp
);

CREATE TABLE replies (
    id serial PRIMARY KEY,
    uid varchar(255) REFERENCES users(uid),
    message_id integer REFERENCES message(id) ON DELETE CASCADE,
    message text,
    created_at timestamp not null default current_timestamp
);


INSERT INTO clubs(club_id,club_name)
VALUES(1,'Baseball'),
      (2,'Soccer'),
      (3,'art'),
      (4,'Judo');

