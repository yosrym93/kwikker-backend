INSERT INTO public.message(
	    from_username, to_username, created_at, text, media_url)
	    VALUES ( 'ahly', 'zamalek', '2015-1-1 4:3:6', 'msg from ahly to zamalek','ahly-zamalek.mediaurl' ),
	           ( 'zamalek', 'ahly', '2014-1-1 4:3:6', 'msg from zamalek to ahly','zamalek-ahly.mediaurl' ),
	           ( 'ahly', 'arsenal', '2011-1-1 4:3:6', 'msg from ahly to arsenal','ahly-zamalek.mediaurl' ),
	           ( 'arsenal', 'ahly', '2012-1-1 4:3:6', 'msg from arsenal to ahly','ahly-zamalek.mediaurl' ),
	           ( 'ahly', 'degla', '2018-1-1 4:3:6', 'msg from ahly to degla','ahly-zamalek.mediaurl' ),
	           ( 'degla', 'ahly', '2016-1-1 4:3:6', 'msg from degla to ahly','ahly-zamalek.mediaurl' );


INSERT INTO public.follow(
	    follower_username, followed_username)
	    VALUES ('zamalek', 'ahly');


INSERT INTO public.mute(
	    muter_username, muted_username)
	    VALUES ('ahly', 'zamalek');


INSERT INTO public.block(
	    blocker_username, blocked_username)
	    VALUES ('ahly', 'zamalek');