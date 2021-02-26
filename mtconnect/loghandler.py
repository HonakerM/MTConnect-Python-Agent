import logging
import os

MTLogger = logging.getLogger(__name__)
level_string = os.getenv('MTCLogLevel','').upper()
level = logging.INFO
if(level_string=='ERROR'):
    level = logging.ERROR
    
elif(level_string=='WARN'):
    level = logging.WARN

elif(level_string=='INFO'):
    level = logging.INFO

elif(level_string=='DEBUG'):
    level = logging.DEBUG

MTLogger.setLevel(level)
