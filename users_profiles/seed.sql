

INSERT INTO user_credentials(
	username, email, password, is_confirmed)
	VALUES ('khaled', 'k@gmail.com', 'kkk', True);
INSERT INTO user_credentials(
	username, email, password, is_confirmed)
	VALUES ('omar', 'o@gmail.com', 'ooo', True);
INSERT INTO user_credentials(
	username, email, password, is_confirmed)
	VALUES ('amr', 'a@gmail.com', 'aaa', True);


INSERT INTO profile(
	username, screen_name, profile_image_url, profile_banner_url, bio, birth_date, created_at)
	VALUES ('khaled', 'gellesh', 'khaledprofile.jpg', 'khaledbanner.jpg', 'he is a man', '1998-12-23', '2004-10-19 10:23:54');
INSERT INTO profile(
	username, screen_name, profile_image_url, profile_banner_url, bio, birth_date, created_at)
	VALUES ('amr', 'bogy', 'profile.jpg', 'banner.png', 'he is a doll', '1998-3-23', '2006-12-19 10:10:24');
INSERT INTO profile(
	username, screen_name, profile_image_url, profile_banner_url, bio, birth_date, created_at)
	VALUES ('omar', '3moar', 'profil.jpg', 'banne.png', 'he is a late man', '1998-3-23', '2001-12-19 10:10:24');

INSERT INTO kweek(
	 created_at, text, media_url, username, reply_to)
	VALUES ( '2019-10-19 10:23:54', 'first kweek','url med1' , 'khaled', null);
INSERT INTO kweek(
	 created_at, text, media_url, username, reply_to)
	VALUES ( '2018-10-1 10:23:54', 'second kweek','url med2' , 'amr', null);
INSERT INTO kweek(
	 created_at, text, media_url, username, reply_to)
	VALUES ( '2019-10-19 10:23:54', 'third kweek','url med3' , 'omar', null);
INSERT INTO kweek(
	 created_at, text, media_url, username, reply_to)
	VALUES ( '2001-10-19 10:23:54', 'fourth kweek','url med4' , 'khaled', null);
INSERT INTO kweek(
	 created_at, text, media_url, username, reply_to)
	VALUES ( '2010-10-19 10:23:54', 'fifth kweek','url med5' , 'khaled', null);


INSERT INTO follow(
	follower_username, followed_username)
	VALUES ('omar', 'khaled');
INSERT INTO follow(
	follower_username, followed_username)
	VALUES ('amr', 'khaled');
INSERT INTO follow(
	follower_username, followed_username)
	VALUES ('amr', 'omar');
INSERT INTO follow(
	follower_username, followed_username)
	VALUES ('omar', 'amr');


INSERT INTO favorite(
	username, kweek_id, created_at)
	VALUES ('khaled', (select id from kweek where username='khaled'and text ='first kweek') ,'2001-12-19 10:10:24' );
INSERT INTO favorite(
	username, kweek_id, created_at)
	VALUES ('khaled', (select id from kweek where username='amr'and text ='second kweek'),'2001-12-19 10:10:24' );
INSERT INTO favorite(
	username, kweek_id, created_at)
	VALUES ('khaled', (select id from kweek where username='omar'and text ='third kweek'),'2001-12-19 10:10:24' );
INSERT INTO favorite(
	username, kweek_id, created_at)
	VALUES ('amr', (select id from kweek where username='khaled'and text ='first kweek'),'2001-12-19 10:10:24' );
INSERT INTO favorite(
	username, kweek_id, created_at)
	VALUES ('amr', (select id from kweek where username='khaled'and text ='fourth kweek'),'2001-12-19 10:10:24' );
INSERT INTO favorite(
	username, kweek_id, created_at)
	VALUES ('omar', (select id from kweek where username='khaled'and text ='fourth kweek'),'2001-12-19 10:10:24' );
