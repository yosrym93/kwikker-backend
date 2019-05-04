insert into user_credentials (username, password, email, is_confirmed)
values ('milan', '$2b$12$NZipoqN11Nr0ftXFKW170OUSn2ZNmDBAaE6tZ8XUlNCuAptpWLtYy', 'acm@gmail.com', True);

INSERT INTO PROFILE(USERNAME, SCREEN_NAME, PROFILE_IMAGE_URL, PROFILE_BANNER_URL, BIO, CREATED_AT, BIRTH_DATE)
VALUES('milan', 'MilanFC',
'http://kwikkerbackend.eu-central-1.elasticbeanstalk.com/user/upload/picture/profile.jpg',
'http://kwikkerbackend.eu-central-1.elasticbeanstalk.com/user/upload/banner/banner.jpg',
'', '2010-01-01', '1998-01-01');
