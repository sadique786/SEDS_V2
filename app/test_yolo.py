from detection.yolo_detector import (
    YOLODetector
)

detector = YOLODetector()

events = detector.detect(
    "test_images/elephant.jpg"
)

print()

print(
    f"Detections: {len(events)}"
)

for event in events:

    print(
        event.object_class,
        round(
            event.confidence,
            2
        )
    )
