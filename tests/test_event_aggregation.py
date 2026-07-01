from datetime import datetime

from app.models import DetectionEvent

from decision.event_manager import (
    EventManager
)

from detection.detection_service import (
    DetectionService
)


manager = EventManager()

service = DetectionService()

event_id = manager.create_event_id()

animals = [

    DetectionEvent(
        timestamp=str(datetime.now()),
        object_class="elephant",
        confidence=0.95,
        image_path="captures/group.jpg",
        event_id=event_id
    ),

    DetectionEvent(
        timestamp=str(datetime.now()),
        object_class="elephant",
        confidence=0.91,
        image_path="captures/group.jpg",
        event_id=event_id
    )
]

for animal in animals:

    service.process_detection(
        animal
    )

print(
    f"Created Event: {event_id}"
)   
