# Table Soccer Elo Rank

Table Soccer Elo Rank is an application to manage and calculate Elo scores in table soccer, keeping track of players' rankings.

## Description

This project aims to provide an Elo scoring system for table soccer, allowing players to record matches, update their Elo scores, and view the overall leaderboard.

## Key Features

- **Elo Score Calculation**: Implementation of the Elo scoring system to determine players' relative strength.
- **Match Management**: Capability to record matches between players, automatically updating Elo scores based on results.
- **Player Leaderboard**: Display of an updated overall leaderboard of players ordered by Elo score.


## Installation

1. Clone the repository:

    ```bash
    git@github.com:F4bio16/table-soccer-elo-rank.git
    ```

2. Install dependencies:

    ```bash
    cd ./table-soccer-elo-rank

    python -m .venv
    source .venv/bin/activate

    pip install -r requirements.txt
    ```

3. Configure environments

    Create file `.env` file:

    ```.env
      DB_NAME=elo-ranking.db
      ELO_MULTIPLIER_FACTOR=32
    ```

    - `DB_NAME` name of SQLite database file
    - `ELO_MULTIPIER_FACTOR` constant K-factor used for Elo algorythm

4. Create database

    ```bash
      source .env
      sqlite3 $DB_NAME < repositories/database.sql
    ```

4. Run the application:

    ```bash
    python .
    ```
