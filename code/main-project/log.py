import os
import sys
import logging
import json

# our costum Json Formatter
class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage()
        }
        return json.dumps(log)

# function to set logging
def setup_logging():

    # env variables
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG")
    LOG_FORMAT = os.environ.get("LOG_FORMAT", "TEXT")

    # logger
    logger = logging.getLogger("myapp")
    logger.setLevel(LOG_LEVEL)

    # standard output handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    
    # custom handler that outputs to file
    file_handler = logging.FileHandler("log.txt")


    if LOG_FORMAT == "JSON":
        # if JSON is chosen, than use JSON Format
        formatter = JsonFormatter()
    else:
        # if not, than using costum text format
        formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(module)s:%(lineno)d:%(funcName)s:%(message)s")

    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger