from datetime import datetime
from database.database_manager import (DatabaseManager)

db = DatabaseManager()

db.insert_detection(
	timestamp=str(datetime.now()),
	object_class="elephant",
	confidence=0.94,
	image_path="captures/test.jpg"
)

detections = db.get_all_detections()
print("\nDetection History\n")

for row in detections:
	print(row)

