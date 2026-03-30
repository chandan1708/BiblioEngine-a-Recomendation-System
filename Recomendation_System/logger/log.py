import logging
import os
from datetime import datetime

LOG_DIR="logs"

LOG_DIR=os.path.join(os.getcwd(),LOG_DIR)

#Creating LOG_DIR if it does not exists
os.makedirs(LOG_DIR,exist_ok=True)

#Creating log file name with timestamp
log_file=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_path=os.path.join(LOG_DIR,log_file)

#Configuring logging
logging.basicConfig(
    filename=log_path,
    format='[%(asctime)s]:%(levelname)s:%(name)s:%(message)s',
    level=logging.NOTSET
)
