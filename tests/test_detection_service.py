from datetime import datetime

from app.models import DetectionEvent

from detection.detection_service import (
    DetectionService
)


service = DetectionService()

event = DetectionEvent(
    timestamp=str(datetime.now()),
    object_class="elephant",
    confidence=0.97,
    image_path="captures/sample.jpg"
)

service.process_detection(event)

print(
    "Detection processed successfully"
)
