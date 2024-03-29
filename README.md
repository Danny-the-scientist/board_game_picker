# Board Game Picker
A python-coded app allowing you populate a local database of your collection and narrow down your choices for a game night. Good times.

## Premise

An SQLite DB (empty XML creation example included) containing a user's board game collection information (exportable from [BoardGameGeek](http://boardgamegeek.com/)) in several tables:
1. Game List - basic information displayed on the BGG header
2. Expansions - tagged, and therefore stored, separately from the main games
3. Ancillary tables - mechanics, categories, etc., which must be obtained through the BGG API

After this DB is populated, running the `streamlit` app will allow you to randomly pick and/or narrow down choices fitting specific criteria.

## Required installed packages

1. `pandas`
2. `streamlit`

Other packages (`sqlite3`, `xml`, `requests`, etc.) should be part of the standard python library, but may be `pip install`ed if needed.

## Usage

First, ensure that your DB path is specified in both `data_populate/sql_tasks.py` and `game_picker/sql_pull.py` and you fill out your BGG username in `data_populate/data_retrieve.py`.

### Filling out the tables

The `data_populate` folder serves two functions relating to the database filling:

1. Compare your current BGG game list to what's in the database, retrieve base information on any missing, assigning them sequential IDs in SQLite
2. Populate category, designer, etc. tables based on the XML from BGG

```bash
cd game-works/data_populate
python3 main.py
```

This will populate the main and auxiliary tables with mechanics, categories, etc. A `sleep` function is included to not overwhelm the BGG API

### Running the app

Locally running the picker app just involves activating streamlit - this will warm the cache on first go and allow the app to be network-accessible.

```bash
cd game-works/game_picker
streamlit run game_picker.py
```
