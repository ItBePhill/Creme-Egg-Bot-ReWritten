import logging
import os
from datetime import date
import colorama

logpath = os.path.join(os.path.dirname(__file__), "Logs/")
logs = len(os.listdir(logpath))

if not os.path.exists(logpath):
    os.makedirs(logpath)

logging.basicConfig(filename=f'{logpath}{logs+1}_{date.today()}_Log.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)


def info(message):
    strmessage = f"{colorama.Fore.BLUE}Info - {colorama.Fore.WHITE}{str(message)}"
    logging.info(str(message))
    print(strmessage)

def warn(message):
    strmessage = f"{colorama.Fore.YELLOW}Warning - {colorama.Fore.WHITE}{str(message)}"
    logging.warn(str(message))
    print(strmessage)

def error(exc):
    logging.error(F"{colorama.Fore.RED}Something Went Wrong!", exc_info=exc)
    print("Something Went Wrong! Check Logs for information")

