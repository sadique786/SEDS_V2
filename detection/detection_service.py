from database.database_manager import DatabaseManager

from app.models import DetectionEvent

from app.utils.logger import setup_logger


class DetectionService:

    def __init__(self):

        self.db = DatabaseManager()

        self.logger = setup_logger()

    def process_detection(
        self,
        event: DetectionEvent
    ):

        self.db.insert_detection(
            timestamp=event.timestamp,
            object_class=event.object_class,
            confidence=event.confidence,
            image_path=event.image_path
        )

        self.logger.info(
            f"{event.object_class} detected "
            f"({event.confidence:.2f})"
        )

        return True
