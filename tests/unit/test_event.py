from app.models import DetectionEvent


event = DetectionEvent(
    timestamp="2026-06-08",
    object_class="elephant",
    confidence=0.95,
    image_path="captures/e1.jpg"
)

print(event)
