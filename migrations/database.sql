CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255),
    surname VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS user_ranks (
    user_id INTEGER,
    points INTEGER NOT NULL,
    created_at INTEGER,
    updated_at INTEGER,
    last_results INTEGER DEFAULT 1,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    state VARCHAR(255),
    expected_scores VARCHAR(255),
    final_result VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS user_games (
    user_id INTEGER,
    game_id INTEGER,
    team VARCHAR(255),
    rank_score INTEGER,
    PRIMARY KEY(user_id, game_id)
);
