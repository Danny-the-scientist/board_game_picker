# Board Game Picker
A python-coded app allowing you to narrow down your board game collection choices for a game night. Good times.

## Premise

An SQLite DB (blank example included) containing a board game collection of information (exportable from [BoardGameGeek](http://boardgamegeek.com/) in several tables:
1. Game List - basic information displayed on the BGG header
2. Expansions - tagged, and therefore stored, separately from the main games
3. Ancillary tables - mechanics, categories, etc., which must be obtained through the BGG API

After this DB is populated, running the `streamlit` app will allow you to randomly pick and/or specifically narrow down choices fitting specific criteria.

## Required installed packages

1. `sqlite3`
2. `pandas`
3. `streamlit`

## Usage

First, ensure that your DB path is specified in both `data_pull/sql_tasks.py` and `game_picker/sql_pull.py`

### Filling out auxiliary tables

Only the main `games_list` table needs to be populated (currently) for the remainder of the module to function. `game_id` needs to be a unique key tracking individual games inside the DB

```bash
cd game-works/data_pull
python3 main.py
```

This will (eventally) populate the auxiliary tables with mechanics, categories, etc. A `sleep` function is included to not overwhelm the BGG API

### Running the app

Locally running the picker app just involves activating streamlit - this will warm the cache on first go and allow the app to be network-accessible. For now, you can see some of my own stuff!

```bash
cd game-works/game_picker
streamlit run game_picker.py
```
