import subprocess
from logging import getLogger
from typing import Tuple

from src.utils.logger import setup_logging

logger = getLogger(__name__)


def run_command(command: str, cwd: str | None = None) -> Tuple[bool, str]:
    setup_logging()
    logger.info(f"Executing command: {command}")
    if cwd:
        logger.info(f"Working directory: {cwd}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd
        )
        output = result.stdout.strip()
        if output:
            logger.debug(f"Command output:\n{output}")
        return True, output
    except subprocess.CalledProcessError as e:
        error_msg = (
            f"Command failed with code {e.returncode}\n"
            f"Output: {e.stdout}\nError: {e.stderr}"
        )
        logger.error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"Error executing command: {str(e)}"
        logger.error(error_msg)
        return False, error_msg