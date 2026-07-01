
from config.config_manager import ConfigManager
from app.utils.logger import setup_logger
from database.database_manager import DatabaseManager


def main():
    print("=" * 60)
    print("🐘 Smart Elephant Detection System v2")
    print("=" * 60)

    logger = setup_logger()
    config = ConfigManager()
    db = DatabaseManager()

    logger.info("SEDS v2 started successfully")

    print("\nSystem initialized successfully")
    print("Configuration loaded")
    print("Logger initialized")
    print("Database connected")

    print("\nReady for AI detection pipeline.")


if __name__ == "__main__":
    main()
