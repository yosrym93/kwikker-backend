
insert into user_credentials(
	username, email, password, is_confirmed )
	VALUES ('khaled', 'k@gmail.com', '$2b$12$y6a/0cxyk5xl3m/O0J9Sf.hE7Af87rdgjljA.kj.nJP3B1KQelvf.', True);
insert into user_credentials(
	username, email, password, is_confirmed )
	VALUES ('omar', 'o@gmail.com', '$2b$12$y6a/0cxyk5xl3m/O0J9Sf.hE7Af87rdgjljA.kj.nJP3B1KQelvf.', True);
insert into user_credentials(
	username, email, password, is_confirmed )
	VALUES ('amr', 'a@gmail.com', '$2b$12$y6a/0cxyk5xl3m/O0J9Sf.hE7Af87rdgjljA.kj.nJP3B1KQelvf.', True);
insert into user_credentials(
	username, email, password, is_confirmed )
	VALUES ('khaled ahmed', 'a@gmail.com', '$2b$12$y6a/0cxyk5xl3m/O0J9Sf.hE7Af87rdgjljA.kj.nJP3B1KQelvf.', True);
insert into user_credentials(
	username, email, password, is_confirmed )
	VALUES ('khaled mohamed', 'a@gmail.com', '$2b$12$y6a/0cxyk5xl3m/O0J9Sf.hE7Af87rdgjljA.kj.nJP3B1KQelvf.', True);
insert into user_credentials(
	username, email, password, is_confirmed )
	VALUES ('mohamed khaled', 'a@gmail.com', '$2b$12$y6a/0cxyk5xl3m/O0J9Sf.hE7Af87rdgjljA.kj.nJP3B1KQelvf.', True);
insert into user_credentials(
	username, email, password, is_confirmed )
	VALUES ('omar@figo', 'f@gmail.com', '$2b$12$y6a/0cxyk5xl3m/O0J9Sf.hE7Af87rdgjljA.kj.nJP3B1KQelvf.', True);
insert into user_credentials(
	username, email, password, is_confirmed )
	VALUES ('ahmed_khaled', 'f@gmail.com', '$2b$12$y6a/0cxyk5xl3m/O0J9Sf.hE7Af87rdgjljA.kj.nJP3B1KQelvf.', True);
insert into user_credentials(
	username, email, password, is_confirmed )
	VALUES ('ahmed', 'f@gmail.com', '$2b$12$y6a/0cxyk5xl3m/O0J9Sf.hE7Af87rdgjljA.kj.nJP3B1KQelvf.', True);
insert into user_credentials(
	username, email, password, is_confirmed )
	VALUES ('yosry', 'r@gmail.com', '$2b$12$y6a/0cxyk5xl3m/O0J9Sf.hE7Af87rdgjljA.kj.nJP3B1KQelvf.', True);


INSERT INTO profile(
	username, screen_name, profile_image_url, profile_banner_url, bio, birth_date, created_at)
	VALUES ('khaled', 'gellesh', 'profile.jpg', 'banner.jpg', 'he is a man', '1998-12-23', '2006-12-19 10:10:24');
INSERT INTO profile(
	username, screen_name, profile_image_url, profile_banner_url, bio, birth_date, created_at)
	VALUES ('amr', 'bogy', 'profile.jpg', 'banner.png', 'he is a doll', '1998-3-23', '2006-12-19 10:10:24');
INSERT INTO profile(
	username, screen_name, profile_image_url, profile_banner_url, bio, birth_date, created_at)
	VALUES ('omar', '3moar', 'profile.jpg', 'banner.png', 'he is a late man', '1998-3-23', '2006-12-19 10:10:24');
insert into profile(
	username, screen_name, profile_image_url, profile_banner_url, bio, birth_date, created_at)
	VALUES ('omar@figo', 'omar_figo', 'profile.jpg', 'banner.png', '', '1998-3-23', '2006-12-19 10:10:24');
insert into profile(
	username, screen_name, profile_image_url, profile_banner_url, bio, birth_date, created_at)
	VALUES ('ahmed_khaled', '@ahmed_khaled', 'profile.jpg', 'banner.png', '', '1998-3-23', '2006-12-19 10:10:24');
insert into profile(
	username, screen_name, profile_image_url, profile_banner_url, bio, birth_date, created_at)
	VALUES ('ahmed', 'mido', 'profile.jpg', 'banner.png', '', '1998-3-23', '2006-12-19 10:10:24');
insert into profile(
	username, screen_name, profile_image_url, profile_banner_url, bio, birth_date, created_at)
	VALUES ('yosry', '@yosry', 'profile.jpg', 'banner.png', '', '1998-3-23', '2006-12-19 10:10:24');
insert into profile(
	username, screen_name, profile_image_url, profile_banner_url, bio, birth_date, created_at)
	VALUES ('khaled ahmed', 'screen_name1', 'profile.jpg', 'banner.png', '', '1998-3-23', '2006-12-19 10:10:24');
insert into profile(
	username, screen_name, profile_image_url, profile_banner_url, bio, birth_date, created_at)
	VALUES ('khaled mohamed', 'screen_name1', 'profile.jpg', 'banner.png', '', '1998-3-23', '2006-12-19 10:10:24');
insert into profile(
	username, screen_name, profile_image_url, profile_banner_url, bio, birth_date, created_at)
	VALUES ('mohamed khaled', 'screen_name1', 'profile.jpg', 'banner.png', '', '1998-3-23', '2006-12-19 10:10:24');




INSERT INTO follow(
	follower_username, followed_username)
	VALUES ('omar', 'khaled');
INSERT INTO follow(
	follower_username, followed_username)
	VALUES ('amr', 'khaled');
INSERT INTO follow(
	follower_username, followed_username)
	VALUES ('yosry', 'khaled');
INSERT INTO follow(
	follower_username, followed_username)
	VALUES ('omar@figo', 'khaled');
INSERT INTO follow(
	follower_username, followed_username)
	VALUES ('ahmed_khaled', 'khaled');
INSERT INTO follow(
	follower_username, followed_username)
	VALUES ('ahmed', 'khaled');
INSERT INTO follow(
	follower_username, followed_username)
	VALUES ('khaled', 'khaled mohamed');
INSERT INTO follow(
	follower_username, followed_username)
	VALUES ('khaled', 'khaled ahmed');
INSERT INTO follow(
	follower_username, followed_username)
	VALUES ('khaled', 'mohamed khaled');
