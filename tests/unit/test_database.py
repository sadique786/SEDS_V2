from datetime import datetime
from database.database_manager import (DatabaseManager)
from decision.event_manager import (EventManager)

db = DatabaseManager()

manager = EventManager()
event_id = manager.create_event_id()

db.insert_detection(
	timestamp=str(datetime.now()),
	object_class="elephant",
	confidence=0.94,
	image_path="captures/test.jpg",
	event_id=event_id
)

detections = db.get_all_detections()
print("\nDetection History\n")

for row in detections:
	print(row)

