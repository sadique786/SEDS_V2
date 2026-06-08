from datetime import datetime

from app.models import DetectionEvent


class MockDetector:

    def detect(self):

        return DetectionEvent(
            timestamp=str(datetime.now()),
            object_class="elephant",
            confidence=0.92,
            image_path="captures/mock_image.jpg"
        )
