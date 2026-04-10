import sqlite3
import os

class SettingsDatabase:
    def __init__(self):
        self.sqlite=sqlite3.connect('settings.db')
        self.sqlite_cursor=self.sqlite.cursor()

    def create(self):
        self.sqlite_cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS settings(
            id INT PRIMARY KEY NOT NULL,
            download_path TEXT NOT NULL,
            video TEXT NOT NULL,
            audio TEXT NOT NULL,
            select_video INT NOT NULL,
            select_audio INT NOT NULL
            );
            '''
        )
        self.sqlite_cursor.execute(
            '''
            INSERT OR IGNORE INTO settings (id,download_path,video,audio,select_video,select_audio)
            VALUES (1,?,'不指定','mp3',?,?);
            ''',
            (os.path.join(os.path.expanduser("~"), "Downloads"),True,True)
        )
        self.sqlite.commit()

    def return_select_video(self):
        self.sqlite_cursor.execute(
            '''
            SELECT select_video FROM settings;
            '''
            )
        return bool(self.sqlite_cursor.fetchone()[0])

    def return_select_audio(self):
        self.sqlite_cursor.execute(
            '''
            SELECT select_audio FROM settings;
            '''
            )
        return bool(self.sqlite_cursor.fetchone()[0])

    def return_download_path(self):
        self.sqlite_cursor.execute(
            '''
            SELECT download_path FROM settings;
            '''
            )
        return self.sqlite_cursor.fetchone()[0]

    def return_video(self):
        self.sqlite_cursor.execute(
            '''
            SELECT video FROM settings;
            '''
            )
        return self.sqlite_cursor.fetchone()[0]

    def return_audio(self):
        self.sqlite_cursor.execute(
            '''
            SELECT audio FROM settings;
            '''
            )
        return self.sqlite_cursor.fetchone()[0]

    def select_video_updata(self):
        self.sqlite_cursor.execute(
            '''
            UPDATE settings SET select_video=?
            ''',(not self.return_select_video(),)
            )
        self.sqlite.commit()

    def select_audio_updata(self):
        self.sqlite_cursor.execute(
            '''
            UPDATE settings SET select_audio=?
            ''',(not self.return_select_audio(),)
            )
        self.sqlite.commit()

    def download_path_updata(self,path):
        self.sqlite_cursor.execute(
            '''
            UPDATE settings SET download_path=?
            ''',(path,)
            )
        self.sqlite.commit()

    def video_updata(self,video):
        self.sqlite_cursor.execute(
            f'''
            UPDATE settings SET video=?
            ''',(video,)
            )
        self.sqlite.commit()

    def audio_updata(self,audio):
        self.sqlite_cursor.execute(
            f'''
            UPDATE settings SET audio=?
            ''',(audio,)
            )
        self.sqlite.commit()