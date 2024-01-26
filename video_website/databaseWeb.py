import sqlite3
from sqlite3 import dbapi2
from cryptography.fernet import Fernet

class Database:
    def __init__(self):
        # open encrypted database
        self.db_file_location = r"C:\Users\schwa\Desktop\discord_project\LukeBot\LukeBot\databases\database.db"
        
        with open(r"C:\Users\schwa\Desktop\API_KEYS\filekey.key", "rb") as key_file:
            self.key = Fernet(key_file.read())
        
        with open(self.db_file_location, "rb") as db_file:
            original = db_file.read()
        
        decrypted = self.key.decrypt(original)
        
        with open(self.db_file_location, "wb") as dec_file:
            dec_file.write(decrypted)
          
        self.database = (self.db_file_location);
        self.conn = None
        self.curs = None

    def connect(self):
        self.conn = sqlite3.connect(self.database)
        self.curs = self.conn.cursor()

    def close(self):
        # opening the original file to encrypt
        with open(self.db_file_location, 'rb') as file:
            original = file.read()
        
        # encrypting the file
        encrypted = self.key.encrypt(original)
 
        # opening the file in write mode and 
        # writing the encrypted data
        with open(self.db_file_location, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
            
        if self.conn:
            self.conn.close()

    def commit(self):
        if self.conn:
            self.conn.commit()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.commit()
        self.close()


    # get video by video id ( also is video filename )
    @classmethod
    def get_video(cls, id: int):
        with cls() as db:
            db.curs.execute("SELECT rowid, * FROM recording_session_compilations WHERE rowid = ?", (id,))
            video_data = db.curs.fetchone()
            return video_data
    
    @classmethod
    def get_all_videos(cls, username: str):
        with cls() as db:
            visible_videos = []
            db.curs.execute(f"SELECT rowid, * FROM recording_session_compilations")
            all_videodata = db.curs.fetchall()
            db.curs.execute(f"SELECT guilds FROM user_accounts WHERE username = ?", (username,))
            user_data = db.curs.fetchone()
            for video in all_videodata:
                print(video)
                print(video[4])
                print(user_data)
                if video[4] in user_data[0]:
                    visible_videos.append(video)
            return visible_videos

    @classmethod
    def check_search(cls, user_input: str):
        with cls() as db:
            db.curs.execute("SELECT rowid, * FROM recording_session_compilations")
            all_videodata = db.curs.fetchall()
        
            filtered_videos = []
        for video_data in all_videodata:
                if user_input.lower() in str(video_data[1]).lower(): # check if user id in discord id string
                        filtered_videos.append(video_data)
                elif user_input.lower() in str(video_data[3]).lower(): # check if search is in video name
                    filtered_videos.append(video_data) 
        return filtered_videos
                 
    @classmethod
    def get_usernames(cls):
        with cls() as db:
            db.curs.execute("SELECT username FROM user_accounts")
            return db.curs.fetchall()

    @classmethod
    def get_discord_ids(cls):
        with cls() as db:
            db.curs.execute("SELECT discord_id FROM user_accounts")
            return db.curs.fetchall()
    
    @classmethod
    def get_logins(cls): # [[username, password], b, c, ..., z]
        with cls() as db:
            db.curs.execute("SELECT username, password FROM user_accounts")
            logins = db.curs.fetchall()
            return logins
            