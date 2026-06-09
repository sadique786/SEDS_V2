from ultralytics import YOLO

from datetime import datetime

from app.models import DetectionEvent


class YOLODetector:

    def __init__(self):

        self.model = YOLO(
            "yolov8n.pt"
        )

    def detect(
        self,
        image_path
    ):

        results = self.model(
            image_path
        )

        detections = []

        for result in results:

            for box in result.boxes:

                class_id = int(
                    box.cls[0]
                )

                class_name = (
                    self.model.names[
                        class_id
                    ]
                )

                confidence = float(
                    box.conf[0]
                )

                detections.append(

                    DetectionEvent(
                        timestamp=str(
                            datetime.now()
                        ),

                        object_class=class_name,

                        confidence=confidence,

                        image_path=image_path
                    )
                )

        return detections
