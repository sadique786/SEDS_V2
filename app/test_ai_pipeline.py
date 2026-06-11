from detection.yolo_detector import YOLODetector
from detection.detection_service import (DetectionService)
from decision.rules_engine import (RulesEngine)


detector = YOLODetector()

rules = RulesEngine()

service = DetectionService()

events = detector.detect("test_images/elephant.jpg")

accepted = 0

for event in events:
	if rules.validate_detection(
		event.object_class,
		event.confidence
	):

	        service.process_detection(event)

        	accepted += 1


print(f"Accepted detections: {accepted}")
