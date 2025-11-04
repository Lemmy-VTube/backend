from logging import getLogger

import uvicorn

from src.config import config
from src.utils.logger import setup_logging

logger = getLogger(__name__)


def start() -> None:
    setup_logging()
    
    try:
        logger.info("Starting backend server...")
        logger.info(f"Host: {config.APP_HOST}, Port: {config.APP_PORT}")
        logger.info(f"Reload mode: {config.APP_RELOAD}")
        logger.info("Server is starting...")
        
        uvicorn.run(
            "src.app:app", 
            host=config.APP_HOST, 
            port=config.APP_PORT, 
            reload=config.APP_RELOAD,
            log_config=None,
            access_log=True,
        )
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        logger.info("Backend terminated with an error")
        raise
    finally:
        logger.info("Backend has stopped")


if __name__ == "__main__":
    start()