import logs
import multiprocessing
import time
from colorama import init, Fore
def StartBot(process):
    from Creme_Egg_Bot_ReWritten import runbot
    runbot(process)
botprocess = None
botprocess = multiprocessing.Process(target = StartBot, name = "Bot Process", daemon = True, args= [botprocess])
if __name__ == "__main__":
    init(convert=True)
    logs.info(Fore.RED+"""
    ___                     ___             ___      _     ___   __      __   _ _   _              
   / __|_ _ ___ _ __  ___  | __|__ _ __ _  | _ ) ___| |_  | _ \__\ \    / / _(_) |_| |_ ___ _ _    
  | (__| '_/ -_) '  \/ -_) | _|/ _` / _` | | _ \/ _ \  _| |   / -_) \/\/ / '_| |  _|  _/ -_) ' \   
   \___|_| \___|_|_|_\___| |___\__, \__, | |___/\___/\__| |_|_\___|\_/\_/|_| |_|\__|\__\___|_||_|  
                                |___/|___/                                                         
                             
    \n""")
    logs.info(Fore.WHITE+f"\nCPU Cores: {multiprocessing.cpu_count()}") 
    botprocess.start()


    while True:
        continue