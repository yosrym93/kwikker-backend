INSERT INTO public.USER_CREDENTIALS
    (USERNAME, PASSWORD, EMAIL, IS_CONFIRMED)
    VALUES ('ahly', '$2b$12$2Pz5Czsrn0MXX/BEqwDgteW8guZgDnB75Ho4rWtfquttl1GMWR2vS', 'ahly@test.com', TRUE),
           ('zamalek', '$2b$12$REZtbFGM6vAq2kIlACyefum2lYtkxkpuE1/Ex68qAk..fqFbeB3pa', 'zamalek@test.com', TRUE),
           ('arsenal', '$2b$12$eH5qw68NWhkwO1jjg2KAxuER1abR.jjmxR7p2/jruyKClZRGG9lFy', 'arsenal@test.com', TRUE),
           ('degla', '$2b$12$8vECtvniAYT7YFcDJBtgveIXgd6N4ai21il1VnpKanjve00rwlzrW', 'degla@test.com', TRUE),
           ('no_message', '$2b$12$lHIyXnMiK/okqQhrNoqXwunl2dAb/.Lo2JtF1zWkuyyY0uVMK3SEW', 'no_message@test.com', TRUE);


INSERT INTO public.profile(
	username, screen_name, profile_image_url, profile_banner_url, bio, created_at, birth_date)
	VALUES ('ahly','ahlyscreenname','ahly.profile.com','ahly.banner.com','ahly bio','1998-3-3 00:00:00', '2000-01-01'),
		   ('zamalek','zamalekscreenname','zamalek.profile.com','zamalek.banner.com','zamalek bio','2001-5-5 5:7:9', '2000-01-01'),
		   ('arsenal','arsenalscreenname','arsenal.profile.com','arsenal.banner.com','arsenal bio','1901-5-5 5:5:5', '2000-01-01'),
	       ('degla','deglascreenname','degla.profile.com','degla.banner.com','degla bio','2015-1-1 4:3:6', '2000-01-01'),
	       ('no_message','no_mess_screenname','no_mess.profile.com','no_mess.banner.com','no_mess bio','2015-1-1 4:3:6', '2000-01-01');

INSERT INTO public.message(
	    from_username, to_username, created_at, text, media_url,is_seen)
	    VALUES ( 'ahly', 'zamalek', '2015-1-1 4:3:6', 'msg from ahly to zamalek','ahly-zamalek.mediaurl', FALSE ),
	           ( 'zamalek', 'ahly', '2014-1-1 4:3:6', 'msg from zamalek to ahly','zamalek-ahly.mediaurl', TRUE ),
	           ( 'ahly', 'arsenal', '2011-1-1 4:3:6', 'msg from ahly to arsenal','ahly-zamalek.mediaurl', TRUE ),
	           ( 'arsenal', 'ahly', '2012-1-1 4:3:6', 'msg from arsenal to ahly','ahly-zamalek.mediaurl', TRUE ),
	           ( 'ahly', 'degla', '2018-1-1 4:3:6', 'msg from ahly to degla','ahly-zamalek.mediaurl', TRUE ),
	           ( 'degla', 'ahly', '2016-1-1 4:3:6', 'msg from degla to ahly','ahly-zamalek.mediaurl', TRUE );


INSERT INTO public.follow(
	    follower_username, followed_username)
	    VALUES ('zamalek', 'ahly');


INSERT INTO public.mute(
	    muter_username, muted_username)
	    VALUES ('ahly', 'zamalek');


INSERT INTO public.block(
	    blocker_username, blocked_username)
	    VALUES ('ahly', 'zamalek');

INSERT INTO public.kweek(
	    created_at, text, media_url, username, reply_to)
	    VALUES ('2010-1-1', 'kweek of 2010','www.media_url.2010','ahly',null),
		   ('2014-4-4', 'kweek of 2014','www.media_url.2014','zamalek',null),
		   ('2018-7-5', 'kweek of 2014','www.media_url.2018','degla',null);