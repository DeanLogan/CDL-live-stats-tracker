import sqlite3

conn = sqlite3.connect('db/cdl-database.db')
db = conn.cursor()

# Create Team table
db.execute('''CREATE TABLE IF NOT EXISTS Team (
            team_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            venues TEXT NOT NULL,
            joined INTEGER DEFAULT 2020,
            owner TEXT NOT NULL,
            series_wins INTEGER DEFAULT 0,
            series_losses INTEGER DEFAULT 0,
            hardpoint_wins INTEGER DEFAULT 0,
            hardpoint_losses INTEGER DEFAULT 0,
            snd_wins INTEGER DEFAULT 0,
            snd_losses INTEGER DEFAULT 0,
            control_wins INTEGER DEFAULT 0,
            control_losses INTEGER DEFAULT 0
        )''')

# Create Player table with foreign key constraint
db.execute('''CREATE TABLE IF NOT EXISTS Player (
            player_id INTEGER PRIMARY KEY,
            handle TEXT NOT NULL,
            name TEXT NOT NULL,
            nationality TEXT NOT NULL,
            avg_overall_kd REAL,
            avg_hardpoint_kd REAL,
            avg_snd_kd REAL,
            avg_control_kd REAL,
            team_name TEXT,
            FOREIGN KEY (team_name) REFERENCES Team(name)
        )''')

conn.commit()
conn.close()
