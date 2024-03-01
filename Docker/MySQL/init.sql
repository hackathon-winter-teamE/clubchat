DROP DATABASE chatapp;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE clubs (
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
    uid varchar(255) REFERENCES users(uid),
    name varchar(255) NOT NULL,
    abstract varchar(255),
    club_id integer REFERENCES clubs(club_id)
);

CREATE TABLE messages (
    id serial PRIMARY KEY,
    uid varchar(255) REFERENCES users(uid),
    cid integer REFERENCES channels(id) ON DELETE CASCADE,
    reply_id integer,
    message text,
    created_at timestamp not null default current_timestamp
);

CREATE TABLE replies (
    id serial PRIMARY KEY,
    user_name varchar(255),
    reply_id integer NOT NULL,
    message text REFERENCES messages(message) ON DELETE CASCADE
);

INSERT INTO users(uid,user_name,email,password,club_id)
VALUES('8defdaea-b411-43d3-8521-db7dc88e633b','na','ff@gmail.com','1234',1);

INSERT INTO channels(id,uid,name,abstract,club_id)
VALUES(1,'','TEST','',1),
      (2,'','TEST','',2),
      (3,'','TEST','',3),
      (4,'','TEST','',4),
      (5,'','TEST','',5),
      (6,'','TEST','',6),
      (7,'','TEST','',7),
      (8,'','TEST','',8),
      (9,'','TEST','',9),
      (10,'','TEST','',10),
      (11,'','TEST','',11),
      (12,'','TEST','',12),
      (13,'','TEST','',13),
      (14,'','TEST','',14),
      (15,'','TEST','',15),
      (16,'','TEST','',16),
      (17,'','TEST','',17),
      (18,'','TEST','',18),
      (19,'','TEST','',19),
      (20,'','TEST','',20),
      (21,'','TEST','',21),
      (22,'','TEST','',22),
      (23,'','TEST','',23),
      (24,'','TEST','',24),
      (25,'','TEST','',25),
      (26,'','TEST','',26),
      (27,'','TEST','',27),
      (28,'','TEST','',28);

INSERT INTO clubs(club_id,club_name)
VALUES(1,'サッカー部'),
      (2,'バスケットボール部'),
      (3,'ソフトボール部'),
      (4,'バドミントン部'),
      (5,'バレーボール部'),
      (6,'ラグビー部'),
      (7,'剣道部'),
      (8,'卓球部'),
      (9,'弓道部'),
      (10,'柔道部'),
      (11,'水泳部'),
      (12,'空手部'),
      (13,'野球部'),
      (14,'陸上部'),
      (15,'囲碁部'),
      (16,'演劇部'),
      (17,'華道部'),
      (18,'合唱部'),
      (19,'軽音楽部'),
      (20,'茶道部'),
      (21,'将棋部'),
      (22,'書道部'),
      (23,'吹奏楽部'),
      (24,'ダンス部'),
      (25,'美術部'),
      (26,'文芸部'),
      (27,'放送部'),
      (28,'その他');