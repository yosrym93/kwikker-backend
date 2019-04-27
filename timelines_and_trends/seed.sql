INSERT INTO USER_CREDENTIALS(USERNAME, PASSWORD, EMAIL, IS_CONFIRMED) VALUES
('test_user1', '$2b$12$/naY78xtO3Za9yefRig8Ueh/6qHIUt5wXSrFaHd96pwhZgRoWTiVm', 'test_user1@test.com', TRUE),
('test_user2', '$2b$12$/naY78xtO3Za9yefRig8Ueh/6qHIUt5wXSrFaHd96pwhZgRoWTiVm', 'test_user2@test.com', TRUE),
('test_user3', '$2b$12$/naY78xtO3Za9yefRig8Ueh/6qHIUt5wXSrFaHd96pwhZgRoWTiVm', 'test_user3@test.com', TRUE);


INSERT INTO PROFILE(USERNAME, SCREEN_NAME, PROFILE_IMAGE_URL, PROFILE_BANNER_URL, BIO, CREATED_AT, BIRTH_DATE)
VALUES
('test_user1', 'test1', 'http://kwikkerbackend.eu-central-1.elasticbeanstalk.com/user/upload/picture/profile.jpg',
 'http://kwikkerbackend.eu-central-1.elasticbeanstalk.com/user/upload/banner/banner.jpg', 'bio', '2019-01-01', '1999-01-01'),
('test_user2', 'test2', 'http://kwikkerbackend.eu-central-1.elasticbeanstalk.com/user/upload/picture/profile.jpg',
 'http://kwikkerbackend.eu-central-1.elasticbeanstalk.com/user/upload/banner/banner.jpg', 'bio', '2019-01-01', '1999-01-01'),
('test_user3', 'test3', 'http://kwikkerbackend.eu-central-1.elasticbeanstalk.com/user/upload/picture/profile.jpg',
 'http://kwikkerbackend.eu-central-1.elasticbeanstalk.com/user/upload/banner/banner.jpg', 'bio', '2019-01-01', '1999-01-01');

INSERT INTO FOLLOW VALUES
('test_user1', 'test_user3'),
('test_user2', 'test_user3'),
('test_user3', 'test_user1'),
('test_user3', 'test_user2');

INSERT INTO MUTE VALUES
('test_user3', 'test_user2');

INSERT INTO BLOCK VALUES
('test_user2', 'test_user1');

INSERT INTO KWEEK(CREATED_AT, TEXT, USERNAME, REPLY_TO) VALUES
('2010-01-01', 'Test user 1, first kweek', 'test_user1', null),
('2013-01-01', 'Test user 1, second kweek', 'test_user1', null),
('2016-01-01', 'Test user 1, third kweek', 'test_user1', null),
('2011-01-01', 'Test user 2, first kweek @test_user1 #trend', 'test_user2', null);

INSERT INTO KWEEK(CREATED_AT, TEXT, USERNAME, REPLY_TO) VALUES
('2014-01-01', 'Test user 2, second kweek', 'test_user2',
 (SELECT ID FROM KWEEK WHERE KWEEK.TEXT = 'Test user 1, second kweek')),
('2015-01-01', 'Test user 2, third kweek', 'test_user2', null),
('2012-01-01', 'Test user 3, first kweek #trend', 'test_user3', null),
('2017-01-01', 'Test user 3, second kweek', 'test_user3', null),
('2018-01-01', 'Test user 3, third kweek', 'test_user3',
 (SELECT ID FROM KWEEK WHERE KWEEK.TEXT = 'Test user 1, third kweek'));

INSERT INTO MENTION(KWEEK_ID, USERNAME, STARTING_INDEX, ENDING_INDEX) VALUES
((SELECT ID FROM KWEEK WHERE USERNAME = 'test_user2' LIMIT 1), 'test_user1', 25, 35);

INSERT INTO HASHTAG(TEXT) VALUES ('trend'), ('trend2');

INSERT INTO KWEEK_HASHTAG VALUES
((SELECT ID FROM KWEEK WHERE USERNAME = 'test_user3' LIMIT 1),
(SELECT ID FROM HASHTAG WHERE TEXT='trend' LIMIT 1), 25, 30),
((SELECT ID FROM KWEEK WHERE USERNAME = 'test_user2' LIMIT 1),
(SELECT ID FROM HASHTAG WHERE TEXT='trend' LIMIT 1), 37, 42);

INSERT INTO FAVORITE VALUES
('test_user3', (SELECT ID FROM KWEEK WHERE USERNAME = 'test_user1' LIMIT 1), '2011-01-01'),
('test_user3', (SELECT ID FROM KWEEK WHERE USERNAME = 'test_user2' LIMIT 1), '2012-01-01');

INSERT INTO REKWEEK VALUES
('test_user3', (SELECT ID FROM KWEEK WHERE USERNAME = 'test_user1' LIMIT 1), '2011-01-01'),
('test_user1', (SELECT ID FROM KWEEK WHERE USERNAME = 'test_user3' LIMIT 1), '2013-02-01');

INSERT INTO NOTIFICATION(CREATED_AT, NOTIFIED_USERNAME, INVOLVED_USERNAME, INVOLVED_KWEEK_ID, TYPE, IS_SEEN) VALUES
('2011-01-01', 'test_user1', 'test_user2', (SELECT ID FROM KWEEK WHERE TEXT LIKE '%@test_user1%'), 'MENTION', TRUE),
('2018-01-01', 'test_user1', 'test_user3', (SELECT ID FROM KWEEK WHERE TEXT = 'Test user 3, third kweek'),
 'REPLY', FALSE),
('2014-01-01', 'test_user1', 'test_user2', (SELECT ID FROM KWEEK WHERE TEXT = 'Test user 2, second kweek'),
 'REPLY', FALSE);
