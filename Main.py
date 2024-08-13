import logs
import multiprocessing
import time
import schedule
import os
from colorama import init, Fore
def StartBot(process):
    from Creme_Egg_Bot_ReWritten import runbot
    runbot(process)
# purge unlistened-to songs from the songs folder
#unfinished
# def Purge():
#     songsfolder = "/Songs"
#     print("Purging!")
#     for i in os.listdir(songsfolder):
#         print(i)

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
    # schedule.every().day.at("12:10").do(Purge)


    while True:
        # schedule.run_pending()
        # time.sleep(1)
        continue


