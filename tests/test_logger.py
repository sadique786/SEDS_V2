from app.utils.logger import setup_logger

logger = setup_logger()

logger.info("System Started")

logger.warning("Camera Not Connected")

logger.error("Telegram Bot Failed")

print("Log entries written successfully")
