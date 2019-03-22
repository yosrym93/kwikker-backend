INSERT INTO USER_CREDENTIALS
    (USERNAME, PASSWORD, EMAIL, IS_CONFIRMED)
    VALUES ('ahly', 'ahlypassword', 'ahly@test.com', TRUE),
           ('zamalek', 'zamalekpassword', 'zamalek@test.com', TRUE),
           ('arsenal', 'arsenalkpassword', 'arsenal@test.com', TRUE),
           ('kitchen', 'kitchenpassword', 'kitchen@test.com', TRUE);


INSERT INTO public.profile(
	username, screen_name, profile_image_url, profile_banner_url, bio, created_at)
	VALUES ('ahly','ahlyscreenname','ahly.profile.com','ahly.banner.com','ahly bio','1998-3-3 00:00:00'),
		   ('zamalek','zamalekscreenname','zamalek.profile.com','zamalek.banner.com','zamalek bio','2001-5-5 5:7:9'),
		   ('arsenal','arsenalscreenname','arsenal.profile.com','arsenal.banner.com','arsenal bio','1901-5-5 5:5:5'),
	       ('kitchen','kitchenscreenname','kitchen.profile.com','kitchen.banner.com','kitchen bio','2015-1-1 4:3:6');


INSERT INTO public.kweek(
	created_at, text, media_url, username, reply_to)
	VALUES ('2010-1-1', 'kweek of 2010','www.media_url.2010','ahly',3),
		   ('2014-4-4', 'kweek of 2014','www.media_url.2014','zamalek',2),
		   ('2018-7-5', 'kweek of 2014','www.media_url.2018','kitchen',1);


INSERT INTO public.notification(
	created_at, notified_username, involved_username, type, involved_kweek_id, is_seen)
	VALUES ('2010-1-2','ahly','zamalek','REKWEEK',(SELECT ID FROM KWEEK WHERE USERNAME = 'zamalek' LIMIT 1),TRUE),
		   ('2014-4-5','zamalek','kitchen','FOLLOW',null,TRUE),
		   ('2018-8-8','kitchen','ahly','LIKE',(SELECT ID FROM KWEEK WHERE USERNAME = 'ahly' LIMIT 1),FALSE);
