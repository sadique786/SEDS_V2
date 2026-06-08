from detection.mock_detector import MockDetector

from detection.detection_service import (
    DetectionService
)

detector = MockDetector()

service = DetectionService()

event = detector.detect()

service.process_detection(event)

print("Pipeline executed successfully")
