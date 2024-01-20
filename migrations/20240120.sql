ALTER TABLE games DROP COLUMN initial_users_score;
ALTER TABLE games DROP COLUMN delta_users_score;
ALTER TABLE games ADD COLUMN args json default '{}';

INSERT INTO _db_migrations_ (name) VALUES ('20240120.sql');
