import logs
import multiprocessing
import time
logs.info("""
    ___                     ___             ___      _     ___   __      __   _ _   _              
   / __|_ _ ___ _ __  ___  | __|__ _ __ _  | _ ) ___| |_  | _ \__\ \    / / _(_) |_| |_ ___ _ _    
  | (__| '_/ -_) '  \/ -_) | _|/ _` / _` | | _ \/ _ \  _| |   / -_) \/\/ / '_| |  _|  _/ -_) ' \   
   \___|_| \___|_|_|_\___| |___\__, \__, | |___/\___/\__| |_|_\___|\_/\_/|_| |_|\__|\__\___|_||_|  
                                |___/|___/                                                         
                             
\n\n""")
logs.info(f"CPU Cores: {multiprocessing.cpu_count()}")
import Creme_Egg_Bot_ReWritten
def StartBot():
    Creme_Egg_Bot_ReWritten.runbot()
botProcess = multiprocessing.Process(target = StartBot, name = "Main Bot Process",  daemon = True)
botProcess.run()