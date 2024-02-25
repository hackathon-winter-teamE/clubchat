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

INSERT INTO users(uid,user_name,email,password,club_id)
VALUES('8defdaea-b411-43d3-8521-db7dc88e633b','na','ff@gmail.com','1234',1);

INSERT INTO channels(id,uid,name,abstract,club_id)
VALUES(1,'','TEST1','',26),
      (2,'','TEST2','',26),
      (3,'','TEST3','',26),
      (4,'','TEST4','',26),
      (5,'','TEST5','',26),
      (6,'','TEST6','',26),
      (7,'','TEST7','',26),
      (8,'','TEST8','',26),
      (9,'','TEST9','',26),
      (10,'','TEST10','',26),
      (11,'','TEST11','',26),
      (12,'','TEST12','',26),
      (13,'','TEST13','',26),
      (14,'','TEST14','',26),
      (15,'','TEST15','',26),
      (16,'','TEST16','',26),
      (17,'','TEST17','',26),
      (18,'','TEST18','',26),
      (19,'','TEST19','',26),
      (20,'','TEST20','',26),
      (21,'','TEST21','',26),
      (22,'','TEST22','',26),
      (23,'','TEST23','',26);

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