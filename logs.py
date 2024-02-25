import logging
import os
from datetime import date
logpath = os.path.join(os.path.dirname(__file__), "Logs")
logs = len(os.listdir(logpath))

if not os.path.exists(logpath):
    os.makedirs(logpath)

logging.basicConfig(filename=f'{logpath}\\{logs+1} {date.today()} Log.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)


def info(message):
    strmessage = str(message)
    logging.info(strmessage)
    print(strmessage)

def warn(message):
    strmessage = str(message)
    logging.warn(strmessage)
    print(strmessage)

def error(exc):
    logging.error("Something Went Wrong!", exc_info=exc)
    print("Something Went Wrong! Check Logs for information")
