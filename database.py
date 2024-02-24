import sqlite3 as sql
import time
import os
import logs
class db():
    def DB(self, title):
        connection = sql.connect("songs.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS SONGS ('id' int, 'filename' varchar(255), 'title' varchar(255), 'url' varchar(255), 'author' varchar(255), 'coverart' varchar(255), 'dur' float, 'last_played' float, 'times_played' int, 'cached' int)")
        titles = cursor.execute('SELECT "title" FROM SONGS')
        titles2 = []
        titles3 = []
        for i in titles:
            titles2.append(i)
        for i in titles2:
            titles3.append(i[0])
        try:
            index = titles3.index(title)
        except Exception as e:
            logs.info(e)
            return None
        else:
            logs.info(f"Found {title}")
            return self.update(self, title, index, connection, cursor)


    
    def add(self, song):
        connection = sql.connect("songs.db")
        cursor = connection.cursor()
        logs.info("Adding a song to the database")
        indexes = cursor.execute('SELECT MAX("id") FROM SONGS')
        indexes2 = []
        for i in indexes:
            indexes2.append(i)
        if indexes2[0][0] == None:
            indexes2 = [[-1]]
        logs.info(indexes2)
        cursor.execute("INSERT INTO SONGS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (indexes2[0][0] + 1, song["filename"], song["title"], song["url"], song["author"], song["coverart"], float(song["dur"]), time.time(), 1, 1))
        logs.info("Successfully added song... closing the database")
        connection.commit()
        connection.close()

    def update(self, song, index, connection: sql.Connection, cursor: sql.Cursor):
        timesplayed = cursor.execute('SELECT "times_played" FROM SONGS WHERE "id" = ?', [int(index)])
        timesplayed2 = []
        for i in timesplayed:
            timesplayed2.append(i)
        logs.info(timesplayed2)
        timesplayed = int(timesplayed2[0][0])
        logs.info("Updating a song in the database")
        logs.info(f'Updating Last Played to {time.time()}')
        cursor.execute('UPDATE SONGS SET "last_played" = ? WHERE "id" = ?', (int(time.time()), int(index)))
        logs.info(f'Updating Times PLayed to {timesplayed+1}')
        cursor.execute('UPDATE SONGS SET "times_played" = ? WHERE "id" =  ?', (int(timesplayed+1), int(index)))
        logs.info("Successfully updated song... returning the song and closing the database")
        record = cursor.execute('SELECT * FROM SONGS WHERE "id" = ?', [int(index)])
        record2 = []
        for i in record:
            record2.append(i)
        record = record2[0]
        cached = record[9]
        if cached == 0:
            return None
        else:
            endsong = {
                "filename": record[1],
                "title": record[2],
                "url": record[3],
                "author" : record[4],
                "coverart": record[5],
                "dur": record[6],
            }
            return endsong
            
    def load(self):
        logs.info("Loading the database")