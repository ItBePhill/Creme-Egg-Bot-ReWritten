import sqlite3 as sql
import time
import os
import logs
class song():
    @classmethod
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
            return self.update(title, index, connection, cursor)
    @classmethod 
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
    @classmethod
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
        cursor.execute('UPDATE SONGS SET "cached" = ? WHERE "id" =  ?', (1, int(index)))
        connection.commit()
        logs.info("Successfully updated song... returning the song and closing the database")
        record = cursor.execute('SELECT * FROM songs WHERE "id" = ?', [int(index)])
        record2 = []
        for i in record:
            record2.append(i)
        record = record2[0]
        
        cached = record[9]
        if cached == 0:
            connection.close()
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
            connection.close()
            return endsong
    @classmethod
    def load(self):
        logs.info("Loading the database")
        connection = sql.connect("songs.db")
        cursor = connection.cursor()
        database = cursor.execute("select * from SONGS")
        returndatabase = []
        for i in database:
            returndatabase.append(i)
        connection.close()
        return returndatabase
            


# class playlist():
#     @classmethod
#     def DB(self, title):
#         connection = sql.connect("lists.db")
#         cursor = connection.cursor()
#         cursor.execute("CREATE TABLE IF NOT EXISTS LISTS VALUES ('id' int, 'path' varchar(255), 'name' varchar(255), 'author' varchar(255), 'cached' int, 'last_played' float, 'times_played' int)")
#         titles = cursor.execute('SELECT "name" FROM LISTS')
#         titles2 = []
#         titles3 = []
#         for i in titles:
#             titles2.append(i)
#         for i in titles2:
#             titles3.append(i[0])
#         try:
#             index = titles3.index(title)
#         except Exception as e:
#             logs.info(e)
#             return None
#         else:
#             logs.info(f"Found {title}")
#             return self.update(title, index, connection, cursor)
        
#     @classmethod
#     def add(self, plist):
#         connection = sql.connect("lists.db")
#         cursor = connection.cursor()
#         logs.info("Adding a list to the database")
#         indexes = cursor.execute('SELECT MAX("id") FROM LISTS')
#         indexes2 = []
#         for i in indexes:
#             indexes2.append(i)
#         if indexes2[0][0] == None:
#             indexes2 = [[-1]]
#         logs.info(indexes2)
#         cursor.execute("INSERT INTO LISTS VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (indexes2, plist["path"], plist["name"], plist["author"], plist["cached"], plist["last_played"], plist["times_played"]))
#         logs.info("Successfully added list... closing the database")
#         connection.commit()
#         connection.close()

#     @classmethod
#     def update(self, index, connection: sql.Connection, cursor: sql.Cursor):
#         timesplayed = cursor.execute('SELECT "times_played" FROM LISTS WHERE "id" = ?', [int(index)])
#         timesplayed2 = []
#         for i in timesplayed:
#             timesplayed2.append(i)
#         logs.info(timesplayed2)
#         timesplayed = int(timesplayed2[0][0])
#         logs.info("Updating a playlist in the database")
#         logs.info(f'Updating Last Played to {time.time()}')
#         cursor.execute('UPDATE LISTS SET "last_played" = ? WHERE "id" = ?', (int(time.time()), int(index)))
#         logs.info(f'Updating Times PLayed to {timesplayed+1}')
#         cursor.execute('UPDATE LISTS SET "times_played" = ? WHERE "id" =  ?', (int(timesplayed+1), int(index)))
#         logs.info("Successfully updated list... returning the list and closing the database")
#         record = cursor.execute('SELECT * FROM LISTS WHERE "id" = ?', [int(index)])
#         record2 = []
#         for i in record:
#             record2.append(i)
#         record = record2[0]
#         cached = record[9]
#         if cached == 0:
#             return None
#         else:
#             endlist = {
#                 "path": record[1],
#                 "name": record[2],
#                 "author": record[3],
#                 "cached": record[4],
#                 "last_played": record[5],
#                 "times_played": record[6]
#             }
#             return endlist
#     @classmethod
#     def load(self):
#         pass


class ShowData():
    @classmethod
    def DB(self, action, show: dict):
        connection = sql.connect("songs.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS SHOWDATA ('id' int, 'name' varchar(255), 'episode' varchar(255), 'time' varchar(255))")
        connection.commit()
        if action == "a":
            self.add(show)
        elif action == "u":
            data = cursor.execute("select name from SHOWDATA")
            data2 = []
            for i in data:
                data2.append(i)
            self.update(show, data2.index(list(show.values())[0]))
    @classmethod
    def add(self, show):
        connection = sql.connect("songs.db")
        cursor = connection.cursor()
        data = cursor.execute("select * from SHOWDATA")
        datadecode = []
        for i in data:
            datadecode.append(i)

        indexes = cursor.execute('SELECT MAX("id") FROM SHOWDATA')
        indexes2 = []
        for i in indexes:
            indexes2.append(i)
        if indexes2[0][0] == None:
            indexes2 = [[-1]]
        if not show in datadecode:
            cursor.execute("INSERT INTO SHOWDATA VALUES(?,?,?,?)", (indexes2[0][0] + 1, show["name"], show["episode"], show["time"]))
        connection.commit()
        connection.close()

    @classmethod
    def update(self, show: dict, index: int):
        connection = sql.connect("songs.db")
        cursor = connection.cursor()
        data = cursor.execute("select * from SHOWDATA")
        datadecode = []
        for i in data:
            datadecode.append(i)
        
        

        logs.info("Updating the show!")
        cursor.execute("UPDATE SHOWDATA SET 'name' = ?, 'episode' = ?, 'time' = ? WHERE 'id' = ?", (show["name"], show["episode"], show["time"], index))
        connection.commit()
        connection.close()
    @classmethod
    def load(self):
        logs.info("Loading the database")
        connection = sql.connect("songs.db")
        cursor = connection.cursor()
        database = cursor.execute("select * from SHOWDATA")
        returndatabase = []
        for i in database:
            returndatabase.append({"name":i[1], "episode":i[2], "time":i[3]})
        
            
        connection.close()
        return returndatabase
    

    # Finish 
    @classmethod
    def remove(self, show):
        pass
    


     