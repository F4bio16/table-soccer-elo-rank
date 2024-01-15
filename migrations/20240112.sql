CREATE TABLE IF NOT EXISTS _db_migrations_ (name VARCHAR(255) unique, created_at DATETIME DEFAULT (DATETIME('NOW', 'localtime')));

INSERT INTO _db_migrations_ (name) VALUES ('database.sql');

CREATE TABLE IF NOT EXISTS games_tmp (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    state VARCHAR(255),
    initial_users_score VARCHAR(255) null,
    delta_users_score VARCHAR(255) null,
    expected_scores VARCHAR(255),
    final_result VARCHAR(255),
    created_at DATETIME DEFAULT (DATETIME('NOW', 'localtime')),
    end_at DATETIME NULL
);

INSERT INTO games_tmp (id, state, expected_scores, final_result) SELECT id, state, expected_scores, final_result FROM games;
ALTER TABLE games RENAME TO games_bkp;
ALTER TABLE games_tmp RENAME TO games;

CREATE TABLE IF NOT EXISTS game_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER,
    user_id INTEGER,
    initial_score INTEGER,
    earned_score INTEGER null,
    created_at DATETIME DEFAULT (DATETIME('NOW', 'localtime')),
    FOREIGN KEY(game_id) REFERENCES games(id)
    FOREIGN KEY(user_id) REFERENCES users(id)
);

ALTER TABLE user_games RENAME TO user_games_bkp;

CREATE TABLE user_games (
    game_id INTEGER,
    user_id INTEGER,
    team VARCHAR(255),
    initial_score INTEGER,
    earned_score INTEGER null,
    created_at DATETIME DEFAULT (DATETIME('NOW', 'localtime')),
    PRIMARY KEY(user_id, game_id)
    FOREIGN KEY(game_id) REFERENCES games(id)
    FOREIGN KEY(user_id) REFERENCES users(id)
);

INSERT INTO user_games (game_id, user_id, team,
    initial_score, earned_score
) SELECT game_id, user_id, team, -1, rank_score FROM user_games_bkp;

INSERT INTO _db_migrations_ (name) VALUES ('20240112.sql');
