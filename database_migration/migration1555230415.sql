ALTER TABLE BLOCK
DROP CONSTRAINT block_blocked_username_fkey,
ADD CONSTRAINT block_blocked_username_fkey
   FOREIGN KEY (blocked_username)
   REFERENCES user_credentials
   ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE BLOCK
DROP CONSTRAINT block_blocker_username_fkey,
ADD CONSTRAINT block_blocker_username_fkey
   FOREIGN KEY (blocker_username)
   REFERENCES user_credentials
   ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE FAVORITE
DROP CONSTRAINT favorite_username_fkey,
ADD CONSTRAINT favorite_username_fkey
   FOREIGN KEY (username)
   REFERENCES user_credentials
   ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE FOLLOW
DROP CONSTRAINT follow_followed_username_fkey,
ADD CONSTRAINT follow_followed_username_fkey
   FOREIGN KEY (followed_username)
   REFERENCES user_credentials
   ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE FOLLOW
DROP CONSTRAINT follow_follower_username_fkey,
ADD CONSTRAINT follow_follower_username_fkey
   FOREIGN KEY (follower_username)
   REFERENCES user_credentials
   ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE KWEEK
DROP CONSTRAINT kweek_username_fkey,
ADD CONSTRAINT kweek_username_fkey
   FOREIGN KEY (username)
   REFERENCES user_credentials
   ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE MENTION
DROP CONSTRAINT mention_username_fkey,
ADD CONSTRAINT mention_username_fkey
   FOREIGN KEY (username)
   REFERENCES user_credentials
   ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE MESSAGE
DROP CONSTRAINT message_from_username_fkey,
ADD CONSTRAINT message_from_username_fkey
   FOREIGN KEY (from_username)
   REFERENCES user_credentials
   ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE MESSAGE
DROP CONSTRAINT message_to_username_fkey,
ADD CONSTRAINT message_to_username_fkey
   FOREIGN KEY (to_username)
   REFERENCES user_credentials
   ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE MUTE
DROP CONSTRAINT mute_muted_username_fkey,
ADD CONSTRAINT  mute_muted_username_fkey
   FOREIGN KEY (muted_username)
   REFERENCES user_credentials
   ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE MUTE
DROP CONSTRAINT mute_muter_username_fkey,
ADD CONSTRAINT  mute_muter_username_fkey
   FOREIGN KEY (muter_username)
   REFERENCES user_credentials
   ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE NOTIFICATION
DROP CONSTRAINT notification_involved_username_fkey,
ADD CONSTRAINT  notification_involved_username_fkey
   FOREIGN KEY (involved_username)
   REFERENCES user_credentials
   ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE NOTIFICATION
DROP CONSTRAINT notification_notified_username_fkey,
ADD CONSTRAINT  notification_notified_username_fkey
   FOREIGN KEY (notified_username)
   REFERENCES user_credentials
   ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE PROFILE
DROP CONSTRAINT profile_username_fkey,
ADD CONSTRAINT  profile_username_fkey
   FOREIGN KEY (username)
   REFERENCES user_credentials
   ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE REKWEEK
DROP CONSTRAINT rekweek_username_fkey,
ADD CONSTRAINT  rekweek_username_fkey
   FOREIGN KEY (username)
   REFERENCES user_credentials
   ON DELETE CASCADE ON UPDATE CASCADE;