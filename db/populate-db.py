import sqlite3

conn = sqlite3.connect('cdl-database.db')
db = conn.cursor()

# Team information to be added
team_info = [
    ("Atlanta FaZe", "United States Atlanta, GA", "Gateway Center Arena", 2020, "Atlanta Esports Ventures, FaZe Clan"),
    ("Boston Breach", "United States Boston, MA", "MGM Music Hall at Fenway", 2022, "Kraft Sports Group"),
    ("Carolina Royal Ravens", "United States Charlotte, NC", "TBA", 2020, "ReKTGlobal, Inc."),
    ("Los Angeles Guerrillas", "United States Los Angeles, CA", "Shrine Exposition Hall", 2020, "Kroenke Sports & Entertainment"),
    ("Los Angeles Thieves", "United States Los Angeles, CA", "Galen Center", 2021, "100 Thieves"),
    ("Miami Heretics", "United States Miami, FL", "TBA", 2020, "Misfits Gaming, Team Heretics"),
    ("Minnesota ROKKR", "United States Minneapolis, MN", "Mystic Lake Casino Hotel", 2020, "G2 Esports"),
    ("New York Subliners", "United States New York City, NY", "Kings Theatre", 2020, "NYXL"),
    ("OpTic Texas", "United States Dallas, TX", "Esports Stadium Arlington", 2020, "OpTic Gaming"),
    ("Seattle Surge", "United States Seattle, WA", "WaMu Theater", 2020, "The Aquilini Group"),
    ("Toronto Ultra", "Canada Toronto, ON", "Mattamy Athletic Centre", 2020, "OverActive Media"),
    ("Vegas Legion", "United States Las Vegas, NV", "Thomas & Mack Center", 2020, "c0ntact Gaming")
]

# Add team information to the Team table
for info in team_info:
    db.execute("INSERT INTO Team (name, location, venues, joined, owner) VALUES (?, ?, ?, ?, ?)", info)


# Player information to be added
player_info = [
    ("aBeZy", "Pharris, Tyler", "United States", "Atlanta FaZe"),
    ("Cellium", "Jovel, McArthur", "United States", "Atlanta FaZe"),
    ("Drazah", "Jordan, Zack", "United States", "Atlanta FaZe"),
    ("Simp", "Lehr, Chris", "United States", "Atlanta FaZe"),

    ("Asim", "Asim, Obaid", "Canada", "Boston Breach"),
    ("Priestahh", "Greiner, Preston", "United States", "Boston Breach"),
    ("SlasheR", "Liddicoat, Austin", "United States", "Boston Breach"),
    ("Snoopy", "Pérez, Eric", "Mexico", "Boston Breach"),

    ("Clayster", "Eubanks, James", "United States", "Carolina Royal Ravens"),
    ("FeLo", "Johnson, Tyler", "United States", "Carolina Royal Ravens"),
    ("Gwinn", "Gwinn, Isiah", "United States", "Carolina Royal Ravens"),
    ("TJHaLy", "Haly, Thomas", "United States", "Carolina Royal Ravens"),

    ("Assault", "Garcia, Adam", "United States", "Los Angeles Guerrillas"),
    ("Diamondcon", "Johst, Conor", "Canada", "Los Angeles Guerrillas"),
    ("Estreal", "McMillan, Justice", "United States", "Los Angeles Guerrillas"),
    ("Fame", "Bonanno, Kevin", "United States", "Los Angeles Guerrillas"),

    ("Afro", "Reid, Marcus", "England", "Los Angeles Thieves"),
    ("Ghosty", "Rothe, Daniel", "United States", "Los Angeles Thieves"),
    ("Kremp", "Haworth, Kyle", "United States", "Los Angeles Thieves"),
    ("Nastie", "Plumridge, Byron", "England", "Los Angeles Thieves"),

    ("EriKBooM", "Ferrer, Eric", "Spain", "Miami Heretics"),
    ("Lucky", "López, Alejandro", "Spain", "Miami Heretics"),
    ("MettalZ", "Serrano, Adrian", "Spain", "Miami Heretics"),
    ("Vikul", "Milagro, Javier", "Spain", "Miami Heretics"),

    ("Accuracy", "Abedi, Lamar", "United States", "Minnesota ROKKR"),
    ("Lynz", "Gregorio, Thomas", "France", "Minnesota ROKKR"),
    ("Owakening", "Conley, Joseph", "United States", "Minnesota ROKKR"),
    ("Vivid", "Drost, Reese", "United States", "Minnesota ROKKR"),

    ("HyDra", "Rusiewiez, Paco", "France", "New York Subliners"),
    ("KiSMET", "Tinsley, Matthew", "United States", "New York Subliners"),
    ("Sib", "Gray, Daunte", "United States", "New York Subliners"),
    ("Skyz", "Bueno, Cesar", "United States", "New York Subliners"),

    ("Dashy", "Otell, Brandon", "Canada", "OpTic Texas"),
    ("Kenny", "Williams, Kenneth", "United States", "OpTic Texas"),
    ("Pred", "Zulbeari, Amer", "Australia", "OpTic Texas"),
    ("Shotzzy", "Cuevas, Anthony", "United States", "OpTic Texas"),

    ("Abuzah", "François, Jordan", "Belgium", "Seattle Surge"),
    ("Arcitys", "Sanderson, Alec", "United States", "Seattle Surge"),
    ("Breszy", "Breszynski, Paul", "France", "Seattle Surge"),
    ("Huke", "Garland, Cuyler", "United States", "Seattle Surge"),

    ("CleanX", "Jønsson, Tobias", "Denmark", "Toronto Ultra"),
    ("Envoy", "Hannon, Dylan", "United States", "Toronto Ultra"),
    ("Insight", "Craven, Jamie", "England", "Toronto Ultra"),
    ("Scrap", "Ernst, Thomas", "United States", "Toronto Ultra"),

    ("Attach", "Price, Dillon", "United States", "Vegas Legion"),
    ("Gio", "Webster, Giovanni", "United States", "Vegas Legion"),
    ("Nero", "Koch, Dylan", "United States", "Vegas Legion"),
    ("Purj", "Perez, Evan", "United States", "Vegas Legion")
]

# Add player information to the Player table
for info in player_info:
    db.execute("INSERT INTO Player (handle, name, nationality, team_name) VALUES (?, ?, ?, ?)", info)

conn.commit()
conn.close()

print("Team and Player information added to the database.")
