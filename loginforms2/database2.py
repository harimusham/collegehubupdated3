import sqlite3

conn = sqlite3.connect('logins2.db', isolation_level=None)
conn.execute("PRAGMA journal_mode=WAL")


conn = sqlite3.connect('logins2.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Facultyss (
        facid INTEGER UNIQUE,
        fusername TEXT,
        fpassword TEXT,
        fname TEXT,
        fdepartment TEXT,
        fdesignation TEXT,
        fmobile INTEGER,
        femail TEXT,
        fspecification TEXT,
        faddress TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Studentss(
        sid INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT,
        name TEXT,
        fathername TEXT,
        mothername TEXT,
        mobilenumber INTEGER,
        pmobilenumber INTEGER,
        dob date,
        gender TEXT,
        email TEXT,
        course TEXT,
        sscmarks INTEGER,
        intermarks INTEGER,
        aadharnumber INTEGER,
        address TEXT,
        city TEXT,
        state TEXT,
        country TEXT,
        registrationapproved TEXT
       
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Markss(
        sid INTEGER PRIMARY KEY,
        semister INTEGER,
        ML INTEGER,
        CD INTEGER,
        SE INTEGER
    )
''' )
cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes(
        fname INTEGER,
        subcode INTEGER,
        subname INTEGER,
        sublink TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobborad(
        jobposition TEXT,
        email TEXT,
        location TEXT,
        salary INTEGER,
        experience INTEGER
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS parents(
        pid INTEGER PRIMARY KEY,
        pusername TEXT,
        ppassword TEXT,
        STUID INTEGER NOT NULL,
        FOREIGN KEY(STUID) REFERENCES Markss(sid)
    )
''' )


cursor.execute('''
    CREATE TABLE IF NOT EXISTS parents (
        pid INTEGER PRIMARY KEY,
        pusername TEXT,
        ppassword TEXT,
        STUID INTEGER NOT NULL,
        FOREIGN KEY(STUID) REFERENCES Markss(sid)
    )
''')








conn.commit()
conn.close()
