import logging 
import os 
from datetime import datetime 


Log_File=f"{datetime.now().strftime('%M_%d_%Y_%H_%M_%S')}.log"
log_path=os.path.join(os.getcwd(),"logs",Log_File)
os.makedirs(log_path,exist_ok=True)


Log_File_Path=os.path.join(log_path,Log_File)


logging.basicConfig(
    filename=Log_File_Path,
    format="[%(asctime)s] %(lineno)d %(name)s-%(levelname)s-%(message)s",
    level=logging.INFO,

)


if __name__=="__main__":
    logging.info("logging has started")



