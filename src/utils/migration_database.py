import argparse
from logging import getLogger

from src.utils.command_runner import run_command
from src.utils.logger import setup_logging

logger = getLogger(__name__)


def main():
    setup_logging()

    parser = argparse.ArgumentParser(description='Database migration tool')
    subparsers = parser.add_subparsers(dest='command', required=True)
    migrate_parser = subparsers.add_parser('commit', help='Run database migrations')
    migrate_parser.add_argument('commit', help='Name of the migration commit')
    
    args = parser.parse_args()
    
    if args.command == 'commit':
        logger.info(f"Starting database migration process: {args.commit}")
        logger.info("Creating database migration...")
        success, output = run_command(f'alembic revision --autogenerate -m "{args.commit}"')
        if not success:
            return logger.error("Migration creation failed")
        
        logger.info("Migration created successfully")
        logger.info("Applying database migration...")
        success, output = run_command('alembic upgrade head')
        if not success:
            return logger.error("Migration application failed")

        logger.info("Migration applied successfully")


if __name__ == "__main__":
    main()