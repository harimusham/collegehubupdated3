import sqlite3

conn = sqlite3.connect('logins3.db', isolation_level=None)
conn.execute("PRAGMA journal_mode=WAL")


conn = sqlite3.connect('logins3.db')
cursor = conn.cursor()

cursor.execute('''
    
    CREATE TABLE "addnewplstudent"(
        plstudent_id INTEGER NOT NULL,
        plsname TEXT NOT NULL,
        plemail TEXT NOT NULL,
        plsphone_number INTEGER NOT NULL,
        plsgender TEXT,
        plsbranch TEXT,
        plsyear_of_passing INTEGER,
        plscompany_name TEXT,
        plsjob_title TEXT,
        plssalary_offered INTEGER,
        plsplacement_date date,
        plsplacement_status TEXT,
        plsresume BLOB,
        plslinkedin TEXT,
        plsgithub TEXT,
        plsskills TEXT
    )
''')

