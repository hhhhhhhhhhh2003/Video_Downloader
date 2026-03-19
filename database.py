from asyncio.windows_events import NULL
import sqlite3
import os

class Database:
    def __init__(self):
        self.settings_sqlite=sqlite3.connect('settings.db')
        self.settings_command=self.settings_sqlite.cursor()
        o=os.path.join(os.path.expanduser('~'),"Downloads")
        self.settings_command.execute('''
        CREATE TABLE IF NOT EXISTS settings(
        id INT PRIMARY KEY NOT NULL,
        download_path TEXT NOT NULL,
        format INT NOT NULL,
        video INT NOT NULL,
        audio INT NOT NULL,
        subtitles TEXT NOT NULL
        );
        ''')
        self.settings_command.execute('''
        INSERT OR IGNORE INTO settings (id,download_path,video,video,audio,subtitles)
        VALUES (?, ?, ?, ?, ?, ?);
        ''',(1,o,1,1,1,'mp4')
        )
        self.settings_sqlite.commit()
        self.library=sqlite3.connect('library.db')
        self.library_command=self.library.cursor()
        self.library_command.execute('''
        CREATE TABLE IF NOT EXISTS library(
        id INT PRIMARY KEY NOT NULL,
        url TEXT NOT NULL
        );
        ''')
        self.library_command.execute('''
        CREATE INDEX idx_url ON library(url)
        ''')
        self.library.commit()

    def return_to_settings(self):
        self.settings_command.execute("SELECT * FROM settings WHERE id=1")
        cursor=self.settings_command.fetchone()
        return cursor

    def modify_settings(self,column,value):
        self.settings_command.execute(f"UPDATE settings SET {column}=?",(value,))
        self.settings_sqlite.commit

    def in_library(self,url):
        self.library_command.execute("SELECT * FROM library WHERE url=?",(url,))
        rows=self.library_command.fetchall
        return bool(rows)

    def add_link(self,url):
        self.library_command.execute("INSERT INTO library (url) VALUES (?)",(url,))
        self.library.commit()