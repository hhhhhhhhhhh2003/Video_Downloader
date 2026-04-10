import sqlite3


class Downloadhistory:
    def __init__(self):
        self.sqlite=sqlite3.connect('history')
        self.sqlite_cursor=self.sqlite.cursor()

    def create(self):
        self.sqlite_cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS history(
            id INT PRIMARY KEY NOT NULL,
            url TEXT NOT NULL,
            title TEXT NOT NULL
            );
            '''
            )
        self.sqlite.commit()

    def indatabase(self,url,title):
        self.sqlite_cursor.execute(
            '''
            SELECT url FROM history WHERE url=? AND title=?
            ''',(url,title)
            )
        return bool(self.sqlite_cursor.fetchone)

    def add(self,url,title):
        self.sqlite_cursor.execute(
            '''
            INSERT INTO COMPANY (url,title) VALUES (?,?)
            ''',
            (url,title)
            )
        self.sqlite.commit()