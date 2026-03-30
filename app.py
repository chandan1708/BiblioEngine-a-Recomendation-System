from Recomendation_System.logger.log import logging
from Recomendation_System.exception.exception_handler import AppException
import sys
# logging.info("Application started")
try:
    a=1
    b=0
    c=a/b
except Exception as e:
    raise AppException(e,sys)
