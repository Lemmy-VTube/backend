import logging

from src.config import config_log


class ColorFormatter(logging.Formatter):
        GREEN = '\033[92m'
        RED = '\033[91m'
        YELLOW = '\033[93m'
        MAGENTA = '\033[95m'
        RESET = '\033[0m'
        
        def format(self, record):
            color = self.RESET
            if record.levelno == logging.INFO:
                color = self.GREEN
            elif record.levelno == logging.ERROR:
                color = self.RED
            elif record.levelno == logging.WARNING:
                color = self.YELLOW
            elif record.levelno == logging.DEBUG:
                color = self.MAGENTA
            
            record.levelname = f"{color}{record.levelname}{self.RESET}"
            record.msg = f"{color}{record.msg}{self.RESET}"
            return super().format(record)


def setup_logging() -> None:
    color_formatter = ColorFormatter(
        fmt=config_log.LOG_FORMAT,
        datefmt=config_log.LOG_DATE_FORMAT
    )
    
    logging.basicConfig(
        level=config_log.LOG_LEVEL,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(config_log.LOG_FILE, encoding='utf-8')
        ]
    )
    
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.setFormatter(color_formatter)