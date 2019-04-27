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

