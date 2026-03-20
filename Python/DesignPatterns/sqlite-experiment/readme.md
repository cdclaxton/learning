# Sqlite experiment for vessel data

Make the virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

Run the experiment:

```bash
python experiment.py
```

Install the `sqlite3` program:

```bash
sudo apt-get install sqlite3
```

Start the SQLite3 program:

```bash
sqlite3 database.db
```

Example SQL queries:

```sql
-- Returns the first 10 vessels
SELECT * FROM vessels LIMIT 10;

-- Returns the first 10 vessels with the name 'vessel-2'
SELECT * FROM vessels WHERE name='vessel-2' LIMIT 10;

-- Number of vessels with name 'vessel-2'
SELECT count(*) FROM vessels WHERE name='vessel-2';
```