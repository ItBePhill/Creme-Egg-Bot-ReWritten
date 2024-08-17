import logs
import multiprocessing
import time
import schedule
import os
import database as db
import time
import sqlite3 as sql
import sys
from colorama import init, Fore
def StartBot(process):
    from Creme_Egg_Bot_ReWritten import runbot
    # runbot(process)
# purge unlistened-to songs from the songs folder
#unfinished
def Purge():
    logs.warn("Killing Bot Process!")
    botprocess.kill()
    database = db.song.load()
    logs.warn("Purging!")
    for song in database:
        if song[9] == 1:
            timesince = time.time() - song[7]
            logs.info(f"Checking: {song[2]}\ntime since last played: ({timesince})")
            if timesince < 0:
                logs.error(f"Last played time is in the future: {time.time() - song[7]}")
            elif timesince >= 2628000: #month in seconds
                connection = sql.connect("songs.db")
                cursor = connection.cursor()
                try:
                    logs.warn(f"Purging: {song[2]}")
                    cursor.execute('UPDATE SONGS SET "cached" = ? WHERE "id" = ?', (0, int(song[0])))
                    connection.commit()   
                    connection.close()             
                except Exception as e:
                    logs.error(e)
                os.remove(song[1])
    logs.warn("Restarting Main.py")
    os.execv(sys.executable, [sys.executable, __file__] + sys.argv)
                



botprocess = None
botprocess = multiprocessing.Process(target = StartBot, name = "Bot Process", daemon = True, args= [botprocess])
if __name__ == "__main__":
    init()
    logs.info(Fore.RED+"""
    ___                     ___             ___      _     ___   __      __   _ _   _              
   / __|_ _ ___ _ __  ___  | __|__ _ __ _  | _ ) ___| |_  | _ \__\ \    / / _(_) |_| |_ ___ _ _    
  | (__| '_/ -_) '  \/ -_) | _|/ _` / _` | | _ \/ _ \  _| |   / -_) \/\/ / '_| |  _|  _/ -_) ' \   
   \___|_| \___|_|_|_\___| |___\__, \__, | |___/\___/\__| |_|_\___|\_/\_/|_| |_|\__|\__\___|_||_|  
                                |___/|___/                                                         
    """)
    logs.info(Fore.WHITE+f"\nCPU Cores: {multiprocessing.cpu_count()}") 
    logs.info(open("Version.txt", "r").read())
    botprocess.start()
    schedule.every().day.at("12:42").do(Purge)


    while True:
        schedule.run_pending()
        time.sleep(1)
        continue


